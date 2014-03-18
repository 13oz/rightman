from rightman.models import *

#user - user object (can django.contrib.auth.User, or not)
#obj - requested object
def can_view(user_acc, obj):
    user_permissions = UserAccounts.objects.filter(user = user_acc)
    if user_permissions.is_root():
        return True
    else:
        return False


def can_modify(user_acc, obj):
    user_permissions = UserAccounts.objects.filter(user = user_acc)
    if user_permissions.is_root():
        return True
    else:
        return False