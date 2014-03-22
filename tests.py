from django.test import TestCase
from rightman.models import *
from rightman import RigthManager

# Create your tests here.
class RigthManagerTestCase(TestCase):
    def setUp(self):
        comp = Company(companyName = "OwnerCorp")
        comp1 = Company(companyName = "TestCorp1")
        comp2 = Company(companyName = "TestCorp2")

        admin_acc = UserAccount(user_role = "0", user_company = comp)

        comp1power_acc = UserAccount(user_role = "1", user_company = comp1)
        comp1power_acc1 = UserAccount(user_role = "1", user_company = comp1)
        comp1user_acc = UserAccount(user_role = "2", user_company = comp1)
        comp1user_acc1 = UserAccount(user_role = "2", user_company = comp1)

        comp2power_acc = UserAccount(user_role = "1", user_company = comp2)
        comp2power_acc1 = UserAccount(user_role = "1", user_company = comp2)
        comp2user_acc = UserAccount(user_role = "2", user_company = comp2)
        comp2user_acc1 = UserAccount(user_role = "2", user_company = comp2)

        public_view_object = Permissions(owner = admin_acc, company = comp, read_permission = "7", modify_permission = "3")
        public_modify_object = Permissions(owner = admin_acc, company = comp, read_permission = "3", modify_permission = "7")

        comp1_user_perm_object = Permissions(owner = comp1user_acc, company = comp1, read_permission = "3", modify_permission = "3")
        comp1_power_perm_object = Permissions(owner = comp1power_acc, company = comp1, read_permission = "6", modify_permission = "6")

        comp2_user_perm_object = Permissions(owner = comp2user_acc, company = comp2, read_permission = "3", modify_permission = "3")
        comp2_power_perm_object = Permissions(owner = comp2power_acc, company = comp2, read_permission = "6", modify_permission = "6")