from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

# Create your models here.
# Company
class Company(models.Model):
    companyName = models.CharField(max_length = 120)

class Permissions(models.Model):
    account = models.ForeignKey(ContentType)
    user_id = models.PositiveIntegerField()
    owner = generic.GenericForeignKey('account', 'user_id')              #must be relation with user model
    company = models.OneToOneField(Company, related_name = 'property_of')
    ruledObject = generic.GenericForeignKey('content_type', 'object_id')

    #return row owner
    def get_owner(self, row_id):
        return User.objects.filter(id=OwnerMixin.objects.filter(id=row_id).owner)

    #this functions checks user roles
    
    #if is superuser
    def is_root(self, user):
        if user.is_superuser():
            return True
        else:
            return False

    #if user in company
    def is_employee(self, user, row_id):
        if user in PowerUsers.objects.filter(company = self.objects.filter(id=row_id)[0].company.companyName) + PlainUsers.objects.filter(company = self.objects.filter(id=row_id)[0].company.companyName):
            return True
        else:
            return False

    #if user is power user
    def is_poweruser(self, user):
        if user in PowerUsers.objects.all():
            return True
        else:
            return False

    #if user is row owner
    def is_owner(self, user, row_id):
        if user in self.get_owner(row_id):
            return True
        else:
            return False


class PowerUsers(models.Model):
    powerUser = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    owner = generic.GenericForeignKey('powerUser', 'object_id')              #must be relation with user model
    company = models.OneToOneField(Company, related_name = 'company_power_user')

    #TODO: def save()
    
    def save(self, *args, **kwargs):
        for elem in PlainUsers.objects.all():
            print self.owner
            print elem.owner
            if self.owner == elem.owner:
                elem.delete()
        super(PowerUsers, self).save(*args, **kwargs)


class PlainUsers(models.Model):
    plainUser = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    owner = generic.GenericForeignKey('plainUser', 'object_id')              #must be relation with user model
    company = models.OneToOneField(Company, related_name = 'company_plain_user')

    #TODO: def save()
    def save(self, *args, **kwargs):
        for elem in PowerUsers.objects.all():
            print self.owner
            print elem.owner
            if self.owner == elem.owner:
                elem.delete()
        super(PlainUsers, self).save(*args, **kwargs)