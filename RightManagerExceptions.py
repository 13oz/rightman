class PermissionNotFoundException(Exception):
    def __init__(self, obj):
        self.req_object = obj

    def __str__(self):
        return  "{} has no permission set".format(repr(self.req_object))

class UserRightNotFoundException(Exception):
    def __init__(self, user):
        self.user_acc = user

    def __str__(self):
        return  "{} has no permission set".format(repr(self.user_acc))

class MultipleRelationWithSingleRemoteObjectException(Exception):
    def __init__(self, remote_obj):
        self.perm_obj = perm_obj
        self.remote_obj = remote_obj

    def __str__(self):
        return  "Permission set for {} is overwritten".format(repr(self.remote_obj))

class MultipleUserPermissionException(Exception):
    def __init__(self, user):
        self.user = user

    def __str__(self):
        return "Permissions for {} is overwritten".format(repr(self.user))