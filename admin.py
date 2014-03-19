from django.contrib import admin
from rightman.models import Company, Permissions, UserAccount

# Register your models here.
admin.site.register(Company)
admin.site.register(Permissions)
admin.site.register(UserAccount)