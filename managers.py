from django.db import models
from django.contrib.auth.models import User

from rightman.models import OwnerMixin

class MixinManager(models.Manager):

    #list all entries
    def all(self, user):
        