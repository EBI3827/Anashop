
from django.urls import path
from .views import ProductDetailView
from .views import home , productlist, contact,product_category,checkout,cart,about_us,compare,search,wishlist

app_name = 'product'

urlpatterns = [
    path('',home, name='home'),
    path('product/<pk>',ProductDetailView.as_view(), name='product-detail'),
    path('products/',productlist, name='products'),
    path('contact-us/',contact, name='contact-us'),
    path('products/<pk>',product_category, name='category'),
    path('checkout/',checkout, name='checkout'),
    path('cart/',cart, name='cart'),
    path('about-us/',about_us, name='about-us'),
    path('compare/',compare, name='copmare'),
    path('search/',search, name='search'),
    path('wishlist/',wishlist, name='wishlist'),

]
