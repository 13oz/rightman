from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from rightman import RightManagerExceptions

# Create your models here.
# Company
class Company(models.Model):
    companyName = models.CharField(max_length = 120)

class UserAccount(models.Model):
    #user roles
    __ADMIN = "admin"
    __POWER = "power user"
    __USER = "user"

    user_roles  = (
        (__ADMIN, "site administrator account"),
        (__POWER, "company administrator account"),
        (__USER, "simple user account"))

    user_object = models.ForeignKey(ContentType)
    user_id = models.PositiveIntegerField()
    user = generic.GenericForeignKey('user_object', 'user_id')
    user_role = models.CharField(max_length = 1, choices = user_roles, default = __USER)
    user_company = models.OneToOneField(Company, related_name = 'employee_of')

    def is_root(self, acc_id):
        if self.objects.filter(id=acc_id)[0].user_roles == __ADMIN:
            return True
        else:
            return False

    def is_power(self, acc_id):
        if self.objects.filter(id=acc_id)[0].user_roles == __POWER:
            return True
        else:
            return False

    def is_user(self, acc_id):
        if self.objects.filter(id=acc_id)[0].user_roles == __USER:
            return True
        else:
            return False

    def employee_of(self, acc_id):
        return self.objects.filter(id=acc_id)[0].user_company

    def save(self, *args, **kwargs):
        for elem in UserAccount.objects.all():
            if self.user == elem.user:
                elem.delete()
                super(UserAccount, self).save(*args, **kwargs)
                raise RightManagerExceptions.MultipleUserPermissionException(self.user)
            else:
                super(UserAccount, self).save(*args, **kwargs)

class Permissions(models.Model):
    #Groups: ANY, COMPANY, OWNER, POWER
    #Actions: READ, MODIFY
    __ANY = "Any"
    __COMPANY = "COMPANY"
    __OWNER = "OWNER"
    __POWER = "POWER"

    read_choise = (
        (__ANY, "Anyone can see this object"),
        (__COMPANY, "This object can be seen only by owner's company employees"),
        (__POWER, "This object can be seen only by company administrators"),
        (__OWNER, "This object can be seen only by it's owner"))

    modify_choise = (
        (__ANY, "Anyone can modify this object"),
        (__COMPANY, "This object can be modfied only be owner's company employees"),
        (__POWER, "This object can be modified only by company administrators"),
        (__OWNER, "This object can be modified only by it's owner"))

    account = models.ForeignKey(ContentType)
    user_id = models.PositiveIntegerField()
    owner = models.OneToOneField(UserAccount, related_name = 'owner')
    company = models.OneToOneField(Company, related_name = 'property_of')
    ruled_object = generic.GenericForeignKey('content_type', 'object_id')
    read_permission = models.CharField(max_length = 2, choices = read_choise, default = COMPANY)
    modify_permission = models.CharField(max_length = 2, choices = modify_choise, default = POWER)

    #return row owner
    def get_owner(self, row_id):
        return self.objects.filter(id=row_id)[0].owner

    def get_read_permission(self, row_id):
        return self.objects.filter(id=row_id)[0].read_permission

    def get_modify_permission(self, row_id):
        return self.objects.filter(id=row_id)[0].modify_permission

    def save(self, *args, **kwargs):
        for elem in Permissions.objects.all():
            if self.ruled_object == elem.ruled_object:
                elem.delete()
                super(Permissions, self).save(*args, **kwargs)
                raise RightManagerExceptions.MultipleRelationWithSingleRemoteObjectException(self.ruled_object)
            else:
                super(Permissions, self).save(*args, **kwargs)