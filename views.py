from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin

from rightman import RightManager

# Create your views here.
class ListViewMixin(ListView):
    #self.model - моделька, которую мы будет показывать
    #TODO возвращает объекты, доступные для просмотра пользователю
    def get(self, request):
        return True

class SingleObjectViewMixin(SingleObjectMixin):
    #self.model - моделька, которую мы будет показывать
    #TODO сделать запрос по фильтру, если имеет права на ЧТЕНИЕ - показать, иначе - 503
    def get_object(self, queryset):
        return True