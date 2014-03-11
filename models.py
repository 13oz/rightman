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
    owner = generic.GenericForeignKey('account', 'user_id')              
    company = models.OneToOneField(Company, related_name = 'property_of')
    ruledObject = generic.GenericForeignKey('content_type', 'object_id')
    #TODO permission bits

    #return row owner
    def get_owner(self, row_id):
        return User.objects.filter(id=OwnerMixin.objects.filter(id=row_id).owner)

    #TODO permission checks


class PowerUsers(models.Model):
    powerUser = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    user = generic.GenericForeignKey('powerUser', 'object_id')              
    company = models.OneToOneField(Company, related_name = 'company_power_user')

    def save(self, *args, **kwargs):
        for elem in PlainUsers.objects.all():
            if self.owner == elem.owner:
                elem.delete()
        for elem in Admins.objects.all():
            if self.owner == elem.owner:
                elem.delete()
        super(PowerUsers, self).save(*args, **kwargs)


class PlainUsers(models.Model):
    plainUser = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    user = generic.GenericForeignKey('plainUser', 'object_id')              
    company = models.OneToOneField(Company, related_name = 'company_plain_user')

    def save(self, *args, **kwargs):
        for elem in PowerUsers.objects.all():
            if self.owner == elem.owner:
                elem.delete()
        for elem in Admins.objects.all():
            if self.owner == elem.owner:
                elem.delete()
        super(PlainUsers, self).save(*args, **kwargs)

class Admins(models.Model):
    plainUser = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    user = generic.GenericForeignKey('plainUser', 'object_id')              
    company = models.OneToOneField(Company, related_name = 'company_plain_user')

    def save(self, *args, **kwargs):
        for elem in PlainUsers.objects.all():
            if self.owner == elem.owner:
                elem.delete()
        for elem in Admins.objects.all():
            if self.owner == elem.owner:
                elem.delete()
        super(PowerUsers, self).save(*args, **kwargs)