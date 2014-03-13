from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

# Create your models here.
# Company
class Company(models.Model):
    companyName = models.CharField(max_length = 120)

class UserAccount(models.Model):
    #user roles
    user_roles  = (
        ("admin", "site administrator account"),
        ("power user", "company administrator account"),
        ("user", "simple user account"))

    user_object = models.ForeignKey(ContentType)
    user_id = models.PositiveIntegerField()
    user = generic.GenericForeignKey('user_object', 'user_id')
    user_role = models.CharField(max_length = 1, choices = user_roles)
    user_company = models.OneToOneField(Company, related_name = 'employee_of')

    def is_root(self, acc_id):
        return True

    def is_power(self, acc_id):
        return True

    def employee_of(self, acc_id):
        return True

class Permissions(models.Model):
    #Groups: ANY, COMPANY, OWNER
    #Actions: READ, MODIFY
    read_choise = (
        ("ANY", "Anyone can see this object"),
        ("COMPANY", "This object can be seen only by owner's company employees"),
        ("OWNER", "This object can be seen only by it's owner"))

    modify_choise = (
        ("ANY", "Anyone can modify this object"),
        ("COMPANY", "This object can be modfied only be owner's company employees"),
        ("OWNER", "This object can be modified only by it's owner"))

    account = models.ForeignKey(ContentType)
    user_id = models.PositiveIntegerField()
    owner = models.OneToOneField(UserAccount, related_name = 'owner')
    company = models.OneToOneField(Company, related_name = 'property_of')
    ruledObject = generic.GenericForeignKey('content_type', 'object_id')
    #TODO permission bits

    #return row owner
    def get_owner(self, row_id):
        return self.objects.filter(id=row_id)[0].owner

    #TODO permission checks