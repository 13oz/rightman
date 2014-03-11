from django.contrib import admin
from rightman.models import Company, PowerUsers, Permissions, PlainUsers

# Register your models here.
admin.site.register(Company)
admin.site.register(PowerUsers)
admin.site.register(PlainUsers)
admin.site.register(Permissions)