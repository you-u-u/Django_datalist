from django.urls import path
from .views import salesrecord_search, salesrecord_list

urlpatterns = [
    path('search/', salesrecord_search, name='salesrecord_search'),
    path('list/', salesrecord_list, name='salesrecord_list'),
]
