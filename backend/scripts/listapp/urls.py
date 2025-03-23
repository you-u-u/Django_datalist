from django.urls import path
from .views.salesrecord import salesrecord_list

urlpatterns = [
    path("salesrecord/list/", salesrecord_list, name="salesrecord_list"),
]
