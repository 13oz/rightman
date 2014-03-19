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
        
#TODO refactor this shit
def can_view(user_acc, obj):
    user_permissions = UserAccounts.objects.filter(user = user_acc)
    if user_permissions.is_root() | is_public(obj):
        return True
    else:
        if obj.read_permission == "6":                                                                #owner + power user
            if user_acc.user_role == "1" & is_employee(user_acc, obj):                                #user is poweruser AND employee
                return True
            elif is_owner(user_acc, obj):
                return True
            else:
                return False
        elif obj.read_permission == "3":                                                             #owner + whole company
            if is_owner(user_acc, obj):
                return True
            elif is_employee(user_acc, obj):
                return True
            else:
                return False


def can_modify(user_acc, obj):
    user_permissions = UserAccounts.objects.filter(user = user_acc)
    if user_permissions.is_root() | is_public(obj):
        return True
    else:
        if obj.modify_permission == "6":                                                                #owner + power user
            if user_acc.user_role == "1" & is_employee(user_acc, obj):                                #user is poweruser AND employee
                return True
            elif is_owner(user_acc, obj):
                return True
            else:
                return False
        elif obj.modify_permission == "3":                                                             #owner + whole company
            if is_owner(user_acc, obj):
                return True
            elif is_employee(user_acc, obj):
                return True
            else:
                return False