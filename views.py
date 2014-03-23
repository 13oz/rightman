from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin

from rightman import RigthManager
from rightman.models import UserAccount, Permissions

# Create your views here.
class ListViewMixin(ListView):
    #self.model - моделька, которую мы будет показывать
    #self.queryset
    #TODO возвращает объекты, доступные для просмотра пользователю
    def get_object():
        if self.request.user.is_authenticated():
            user_perm = UserAccount.objects.filter(user = self.request.user)
            for elem in self.queryset:
                for perm_elem in Permissions.objects.filter(ruled_object = elem):
                    if RightManager.can_view(perm_elem.read_permissions, Permissions.objects.filter(ruled_object = elem)):
                        return super(ListViewMixin, self).get_object(self, *args, **kwargs)
                    else:
                        return False
        else:
            for elem in self.queryset:
                for perm_elem in Permissions.objects.filter(ruled_object = elem):
                    if RightManager.is_public(perm_elem.read_permissions):
                        return super(ListViewMixin, self).get_object(self, *args, **kwargs)
                    else:
                        return False

    def get_queryset(): 
        if self.request.user.is_authenticated():
            return [elem for elem in self.queryset if RigthManager.can_view(UserAccount(user=self.request.user), Permissions.objects.get(ruled_object=elem))]
        else:
            return [elem for elem in self.queryset if RigthManager.is_public(Permissions.objects.get(ruled_object=elem))]

    def form_valid():
        return True

class SingleObjectViewMixin(SingleObjectMixin):
    #self.model - моделька, которую мы будет показывать
    #self.queryset
    #TODO сделать запрос по фильтру, если имеет права на ЧТЕНИЕ - показать, иначе - 503
    def get_object():
        if self.request.user.is_authenticated():
            user_perm = UserAccount.objects.filter(user = self.request.user)
            for elem in self.queryset:
                for perm_elem in Permissions.objects.filter(ruled_object = elem):
                    if RightManager.can_view(perm_elem.read_permissions, Permissions.objects.filter(ruled_object = elem)):
                        return super(ListViewMixin, self).get_object(self, *args, **kwargs)
                    else:
                        return False
        else:
            for elem in self.queryset:
                for perm_elem in Permissions.objects.filter(ruled_object = elem):
                    if RightManager.is_public(perm_elem.read_permissions):
                        return super(ListViewMixin, self).get_object(self, *args, **kwargs)
                    else:
                        return False

    def get_queryset():
        if self.request.user.is_authenticated():
            return [elem for elem in self.queryset if RigthManager.can_view(UserAccount(user=self.request.user), Permissions.objects.get(ruled_object=elem))]
        else:
            return [elem for elem in self.queryset if RigthManager.is_public(Permissions.objects.get(ruled_object=elem))]

    def form_valid():
        return True