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
    __ADMIN = "0"
    __POWER = "1"
    __USER = "2"

    user_roles  = (
        (__ADMIN, "site administrator account"),
        (__POWER, "company administrator account"),
        (__USER, "simple user account"))

    user_object = models.ForeignKey(ContentType)
    user_id = models.PositiveIntegerField()
    user = generic.GenericForeignKey('user_object', 'user_id')
    user_role = models.CharField(max_length = 1, choices = user_roles, default = __USER)
    user_company = models.ForeignKey(Company, unique = False, related_name = 'employee_of')

    def is_root(self):
        if self.user_role == "0":
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

    """def save(self, *args, **kwargs):
                    for elem in UserAccount.objects.all():
                        if self.user == elem.user:
                            elem.delete()
                            super(UserAccount, self).save(*args, **kwargs)
                            raise RightManagerExceptions.MultipleUserPermissionException(self.user)
                        else:
                            super(UserAccount, self).save(*args, **kwargs)"""

class Permissions(models.Model):
    #Groups: ANY, COMPANY, OWNER, POWER
    #Actions: READ, MODIFY
    __COMPANY = "1"
    __OWNER = "2"
    __POWER = "4"

    __COMPANY_OWNER = "3"
    __OWNER_POWER = "6"
    __ANY = "7"
    

    read_choise = (
        (__ANY, "Anyone can see this object"),
        (__COMPANY_OWNER, "This object can be seen by owner and company employees"),
        (__OWNER_POWER, "This object can be seen by owner and company admins"),
        (__COMPANY, "This object can be seen only by owner's company employees"),
        (__POWER, "This object can be seen only by company administrators"),
        (__OWNER, "This object can be seen only by it's owner"))

    modify_choise = (
        (__ANY, "Anyone can modify this object"),
        (__COMPANY_OWNER, "This object can be midified by owner and company employees"),
        (__OWNER_POWER, "This object can be midified by owner and company admins"),
        (__COMPANY, "This object can be modfied only be owner's company employees"),
        (__POWER, "This object can be modified only by company administrators"),
        (__OWNER, "This object can be modified only by it's owner"))

    obj = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    ruled_object = generic.GenericForeignKey('obj', 'object_id')
    owner = models.ForeignKey(UserAccount, related_name = 'owner')
    company = models.ForeignKey(Company, related_name = 'property_of')
    read_permission = models.CharField(max_length = 1, choices = read_choise, default = __COMPANY)
    modify_permission = models.CharField(max_length = 1, choices = modify_choise, default = __POWER)

    """def save(self, *args, **kwargs):
                    for elem in Permissions.objects.all():
                        if self.ruled_object == elem.ruled_object:
                            elem.delete()
                            super(Permissions, self).save(*args, **kwargs)
                            raise RightManagerExceptions.MultipleRelationWithSingleRemoteObjectException(self.ruled_object)
                        else:
                            super(Permissions, self).save(*args, **kwargs)"""