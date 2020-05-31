
from django.urls import path
from .views import ProductListView,ProductDetailView
from .views import home

app_name = 'product'

urlpatterns = [
    path('',home, name='home'),
    path('product/<pk>',ProductDetailView.as_view(), name='product-detail'),
    path('products/',ProductListView.as_view(), name='products'),
]
