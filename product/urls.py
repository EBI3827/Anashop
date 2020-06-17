
from django.urls import path, re_path
from .views import (
    home,
    ProductDetailView,
    productlist,
    contact,
    product_category,
    checkout,
    about_us,
    CompareView, 
    add_to_compare,
    remove_from_compare,
    search, 
    WishView,
    add_to_wishlist,
    remove_from_wishlist,
    product_subcategory,
    sitemap,
)

app_name = 'product'

urlpatterns = [
    path('', home, name='home'),
    path('product/<int:pk>/<slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/', productlist, name='products'),
    path('contact-us/', contact, name='contact-us'),
    path('products/<int:pk>/<slug>/', product_category, name='category'),
    path('products/<slug>/<int:pk>/<category>/', product_subcategory, name='subcategory'),
    path('checkout/', checkout, name='checkout'),
    path('about-us/', about_us, name='about-us'),
    path('sitemap/', sitemap, name='sitemap'),
    path('compare/', CompareView.as_view(), name='compare'),
    path('add_to_compare/<pk>', add_to_compare, name='add_to_compare'),
    path('remove_from_compare/<pk>', remove_from_compare, name='remove_from_compare'),
    path('search/', search, name='search'),
    path('wishlist/', WishView.as_view(), name='wishlist'),
    path('add_to_wishlist/<pk>', add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<pk>', remove_from_wishlist, name='remove_from_wishlist'),

]
