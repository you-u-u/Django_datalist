from django.urls import path, include
from . import views
from .views import SalesByProductView, RecordSearchAPI,search_page
#from .views import salesrecord_search, salesrecord_list
#from rest_framework.routers import DefaultRouter
app_name = 'listapp'

# router = DefaultRouter()
# router.register(r'myendpoint', salesrecord, basename='salesrecord')

urlpatterns = [
    path('', views.Top.as_view(), name='top'),  
    # path('search/', SalesByProductView.as_view(), name='salesrecord_search'),
    #path('list/', SalesRecordList.as_view(), name='list'),
    #path('list/',salesrecord, name='salesrecord_list'), 
    #path('sales/', SalesRecordListView.as_view(), name='sales_list'),
    path('search/', views.search_page, name='search_page'),
    path('sales/', views.RecordSearchAPI.as_view(), name='sales_api'),

]
