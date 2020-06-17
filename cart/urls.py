from django.urls import path, re_path
from .views import CartView, add_to_cart, remove_from_cart,remove_single_item_from_cart

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add_to_cart/<pk>', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<pk>', remove_from_cart, name='remove_from_cart'),
    path('remove_item_from_cart/<pk>/',
         remove_single_item_from_cart,
         name='remove_single_item_from_cart'),
]
