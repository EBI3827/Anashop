
from django.urls import path
from .views import ProductListView
from .views import home

app_name = 'product'
urlpatterns = [
    path('',home, name='home'),
    path('products/',ProductListView.as_view(), name='products'),
]
