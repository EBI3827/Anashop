
from django.urls import path
from .views import ProductDetailView
from .views import home , productlist, contact

app_name = 'product'

urlpatterns = [
    path('',home, name='home'),
    path('product/<pk>',ProductDetailView.as_view(), name='product-detail'),
    path('products/',productlist, name='products'),
    path('contact-us/',contact, name='contact-us'),
]
