from django.urls import path, re_path
from .views import (CartView, add_to_cart, remove_from_cart,
                    remove_single_item_from_cart,AddCouponView, CheckoutView, PaymentView)

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add_to_cart/<pk>', add_to_cart, name='add_to_cart'),
    path('add_coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove_from_cart/<pk>', remove_from_cart, name='remove_from_cart'),
    path('remove_item_from_cart/<pk>/',
         remove_single_item_from_cart,
         name='remove_single_item_from_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),

    # re_path(
    #     r'^country-autocomplete/$',
    #     CountryAutocomplete.as_view(),
    #     name='country-autocomplete',
    # ),
]
