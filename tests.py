from django.test import TestCase
from django.contrib.auth.models import User

from rightman.models import *
from rightman import RigthManager
from testapp.models import Post

# Create your tests here.
class RigthManagerTestCase(TestCase):
    def setUp(self):
        Company.objects.create(companyName = "OwnerCorp")
        Company.objects.create(companyName = "TestCorp1")
        Company.objects.create(companyName = "TestCorp2")

        self.comp1 = Company.objects.get(id=1)                           #OwnerCorp
        self.comp2 = Company.objects.get(id=2)                           #TestCorp1
        self.comp3 = Company.objects.get(id=3)                           #TestCorp2

        UserAccount.objects.create(user_role = "0", user_company = self.comp1, user = User.objects.create(username = "admin", password = "12345"))

        UserAccount.objects.create(user_role = "1", user_company = self.comp2, user = User.objects.create(username = "1power1", password = "12345"))
        UserAccount.objects.create(user_role = "1", user_company = self.comp2, user = User.objects.create(username = "1power2", password = "12345"))
        UserAccount.objects.create(user_role = "2", user_company = self.comp2, user = User.objects.create(username = "1user1", password = "12345"))
        UserAccount.objects.create(user_role = "2", user_company = self.comp2, user = User.objects.create(username = "1user2", password = "12345"))

        UserAccount.objects.create(user_role = "1", user_company = self.comp3, user = User.objects.create(username = "2power1", password = "12345"))
        UserAccount.objects.create(user_role = "1", user_company = self.comp3, user = User.objects.create(username = "2power2", password = "12345"))
        UserAccount.objects.create(user_role = "2", user_company = self.comp3, user = User.objects.create(username = "2user1", password = "12345"))
        UserAccount.objects.create(user_role = "2", user_company = self.comp3, user = User.objects.create(username = "2user2", password = "12345"))

        self.admin_acc = UserAccount.objects.get(id=1)                   #site admin

        self.comp1power_acc = UserAccount.objects.get(id=2)
        self.comp1power_acc1 = UserAccount.objects.get(id=3)
        self.comp1user_acc = UserAccount.objects.get(id=4)
        self.comp1user_acc1 = UserAccount.objects.get(id=5)

        self.comp2power_acc = UserAccount.objects.get(id=6)
        self.comp2power_acc1 = UserAccount.objects.get(id=7)
        self.comp2user_acc = UserAccount.objects.get(id=8)
        self.comp2user_acc1 = UserAccount.objects.get(id=9)

        Post.objects.create(headerField="public", textField="bar")
        self.public_post = Post.objects.get(headerField="public")

        Post.objects.create(headerField = "comp1CW", textField = "bar")
        self.comp1CW = Post.objects.get(headerField="comp1CW")

        Post.objects.create(headerField = "comp1PW", textField = "bar")
        self.comp1PW = Post.objects.get(headerField="comp1PW")

        Post.objects.create(headerField = "comp1UPW", textField = "bar")
        self.comp1UPW = Post.objects.get(headerField="comp1UPW")

        Post.objects.create(headerField = "comp2CW", textField = "bar")
        self.comp2CW = Post.objects.get(headerField="comp2CW")

        Post.objects.create(headerField = "comp2PW", textField = "bar")
        self.comp2PW = Post.objects.get(headerField="comp2PW")

        Post.objects.create(headerField = "comp2UPW", textField = "bar")
        self.comp2UPW = Post.objects.get(headerField="comp2UPW")

        Permissions.objects.create(owner = self.admin_acc, company = self.comp1, read_permission = "7", modify_permission = "7", ruled_object = self.public_post)

        Permissions.objects.create(owner = self.comp1user_acc, company = self.comp2, read_permission = "3", modify_permission = "3", ruled_object = self.comp1CW)
        Permissions.objects.create(owner = self.comp1power_acc, company = self.comp2, read_permission = "6", modify_permission = "6", ruled_object = self.comp1PW)
        Permissions.objects.create(owner = self.comp1user_acc, company = self.comp2, read_permission = "6", modify_permission = "6", ruled_object = self.comp1UPW)

        Permissions.objects.create(owner = self.comp2user_acc, company = self.comp3, read_permission = "3", modify_permission = "3", ruled_object = self.comp2CW)
        Permissions.objects.create(owner = self.comp2power_acc, company = self.comp3, read_permission = "6", modify_permission = "6", ruled_object = self.comp2PW)

        self.public_view_object = Permissions.objects.get(id=1)

        self.comp1_user_perm_object = Permissions.objects.get(id=2)
        self.comp1_power_perm_object = Permissions.objects.get(id=3)
        self.comp1_user_OP_perm_object = Permissions.objects.get(id=4)
        self.comp2_user_perm_object = Permissions.objects.get(id=5)
        self.comp2_power_perm_object = Permissions.objects.get(id=6)

    def test_permission_check(self):    
        self.assertEqual(RigthManager.is_public(self.public_view_object), True)
        self.assertEqual(RigthManager.is_public(self.comp1_user_perm_object), False)

        self.assertEqual(RigthManager.is_owner(self.comp1power_acc, self.comp1_user_perm_object), False)
        self.assertEqual(RigthManager.is_owner(self.comp1user_acc, self.comp1_user_perm_object), True)

        self.assertEqual(RigthManager.is_employee(self.admin_acc, self.public_view_object), True)
        self.assertEqual(RigthManager.is_employee(self.comp1power_acc, self.comp2_power_perm_object), False)

        #admin view access test
        self.assertEqual(RigthManager.can_view(self.admin_acc, self.public_view_object), True)
        self.assertEqual(RigthManager.can_view(self.admin_acc, self.comp1_user_perm_object), True)
        self.assertEqual(RigthManager.can_view(self.admin_acc, self.comp1_power_perm_object), True)

        #admin modify access test
        self.assertEqual(RigthManager.can_modify(self.admin_acc, self.public_view_object), True)
        self.assertEqual(RigthManager.can_modify(self.admin_acc, self.comp1_user_perm_object), True)
        self.assertEqual(RigthManager.can_modify(self.admin_acc, self.comp1_power_perm_object), True)

        #user view access
        self.assertEqual(RigthManager.can_view(self.comp1user_acc, self.public_view_object), True)
        self.assertEqual(RigthManager.can_view(self.comp1user_acc, self.comp1_user_perm_object), True)
        self.assertEqual(RigthManager.can_view(self.comp1user_acc1, self.comp1_user_perm_object), True)
        self.assertEqual(RigthManager.can_view(self.comp1user_acc1, self.comp1_user_OP_perm_object), False)
        self.assertEqual(RigthManager.can_view(self.comp1user_acc, self.comp1_power_perm_object), False)
        self.assertEqual(RigthManager.can_view(self.comp1user_acc, self.comp2_user_perm_object), False)
        self.assertEqual(RigthManager.can_view(self.comp1user_acc, self.comp2_power_perm_object), False)

        #power view access
        self.assertEqual(RigthManager.can_view(self.comp1power_acc, self.public_view_object), True)
        self.assertEqual(RigthManager.can_view(self.comp1power_acc, self.comp1_user_perm_object), True)
        self.assertEqual(RigthManager.can_view(self.comp1power_acc, self.comp1_user_OP_perm_object), True)
        self.assertEqual(RigthManager.can_view(self.comp1power_acc, self.comp1_power_perm_object), True)
        self.assertEqual(RigthManager.can_view(self.comp1power_acc, self.comp2_user_perm_object), False)
        self.assertEqual(RigthManager.can_view(self.comp1power_acc, self.comp2_power_perm_object), False)

        #user modify access
        self.assertEqual(RigthManager.can_modify(self.comp1user_acc, self.public_view_object), True)
        self.assertEqual(RigthManager.can_modify(self.comp1user_acc, self.comp1_user_perm_object), True)
        self.assertEqual(RigthManager.can_modify(self.comp1user_acc1, self.comp1_user_perm_object), True)
        self.assertEqual(RigthManager.can_modify(self.comp1user_acc1, self.comp1_user_OP_perm_object), False)
        self.assertEqual(RigthManager.can_modify(self.comp1user_acc, self.comp1_power_perm_object), False)
        self.assertEqual(RigthManager.can_modify(self.comp1user_acc, self.comp2_user_perm_object), False)
        self.assertEqual(RigthManager.can_modify(self.comp1user_acc, self.comp2_power_perm_object), False)

        #power view access
        self.assertEqual(RigthManager.can_view(self.comp1power_acc, self.public_view_object), True)
        self.assertEqual(RigthManager.can_view(self.comp1power_acc, self.comp1_user_perm_object), True)
        self.assertEqual(RigthManager.can_view(self.comp1power_acc, self.comp1_user_OP_perm_object), True)
        self.assertEqual(RigthManager.can_view(self.comp1power_acc, self.comp1_power_perm_object), True)
        self.assertEqual(RigthManager.can_view(self.comp1power_acc, self.comp2_user_perm_object), False)
        self.assertEqual(RigthManager.can_view(self.comp1power_acc, self.comp2_power_perm_object), False)

        #power modify access
        self.assertEqual(RigthManager.can_modify(self.comp1power_acc, self.public_view_object), True)
        self.assertEqual(RigthManager.can_modify(self.comp1power_acc, self.comp1_user_perm_object), True)
        self.assertEqual(RigthManager.can_modify(self.comp1power_acc, self.comp1_user_perm_object), True)
        self.assertEqual(RigthManager.can_modify(self.comp1power_acc, self.comp1_user_OP_perm_object), True)
        self.assertEqual(RigthManager.can_modify(self.comp1power_acc, self.comp1_power_perm_object), True)
        self.assertEqual(RigthManager.can_modify(self.comp1power_acc, self.comp2_user_perm_object), False)
        self.assertEqual(RigthManager.can_modify(self.comp1power_acc, self.comp2_power_perm_object), False)