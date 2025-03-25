from django.urls import path, include
from . import views
from .views import SalesByProductView, SalesRecordListAPI
#from .views import salesrecord_search, salesrecord_list
#from rest_framework.routers import DefaultRouter
app_name = 'listapp'

# router = DefaultRouter()
# router.register(r'myendpoint', salesrecord, basename='salesrecord')

urlpatterns = [
    path('', views.Top.as_view(), name='top'),  
    path('search/', SalesByProductView.as_view(), name='salesrecord_search'),
    #path('list/', SalesRecordList.as_view(), name='list'),
    #path('list/',salesrecord, name='salesrecord_list'), 
    #path('sales/', SalesRecordListView.as_view(), name='sales_list'),
    path('sales/', SalesRecordListAPI.as_view(), name='sales_api'),

]
