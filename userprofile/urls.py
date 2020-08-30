from django.urls import path, re_path
from .views import userprofile,OrderDetail,UserOrders,UserAddresses,UserComments,PersonalInfo,datepicker

app_name = 'userprofile'

urlpatterns = [
    path('', userprofile, name='userprofile'),
    path('order-detail/<pk>', OrderDetail, name='order-detail'),
    path('user-orders/', UserOrders, name='user-orders'),
    path('addresses/', UserAddresses, name='user-addresses'),
    path('comments/', UserComments, name='user-comments'),
    path('personal-info/', PersonalInfo, name='personal-info'),
    path('datepicker/', datepicker, name='datepicker'),

    

]