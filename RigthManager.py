from rightman.models import *

#user - user object (can django.contrib.auth.User, or not)
#obj - requested object
def can_view(user, obj):
    return True

def can_modify(user, obj):
    return True