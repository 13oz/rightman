from rightman.models import *

#user - user object (can django.contrib.auth.User, or not)
#obj - requested object permission object
def is_public(obj):
    if obj.read_permission == "7":
        return True
    else:
        return False

def is_owner(user_acc, obj):
    if obj.owner == user_acc:
        return True
    else:
        return False

def is_employee(user_acc, obj):
    if user_acc.user_company == obj.company:
        return True
    else:
        return False

def has_permission(obj_permission, user_role, obj_company, user_company):
    if obj_permission == "6":                                                                       #owner + power user
        if user_role == "1" & obj_company == user_company:                                          #user is poweruser AND employee
            return True
        else:
            return False
    if obj_permission == "3":                                                                       #owner + whole company
        if obj_company == user_company:
            return True
        else:
            return False

#TODO refactor this shit
def can_view(user_acc, obj):
    user_permissions = UserAccounts.objects.filter(user = user_acc)
    if user_permissions.is_root() | is_public(obj) | is_owner(user_acc, obj):
        return True
    else:
        return has_permission(obj.read_permission, user_permissions.user_role, obj.company, user_permissions.user_company)


def can_modify(user_acc, obj):
    user_permissions = UserAccounts.objects.filter(user = user_acc)
    if user_permissions.is_root() | is_public(obj) | is_owner(user_acc, obj):
        return True
    else:
        return has_permission(obj.modify_permission, user_permissions.user_role, obj.company, user_permissions.user_company)