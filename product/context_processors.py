from .models import Product, Category, FeatureManager
from cart.models import Order, OrderItem
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from blog.models import Blog
from django.db.models import Count
from django.db.models import Sum
from django.shortcuts import get_object_or_404


def nav(request, *args, **kwargs):
    categories = Category.objects.all()
    order = request.GET.get('order', 'added_date')
    products = Product.objects.all().order_by(order)
    latest = Product.objects.all().order_by('-added_date')[:6]
    blogs = Blog.objects.all().order_by('date')[:3]
    popular_products = Product.objects.order_by(
        '-hit_count_generic__hits')[:10]
    featured = Product.objects.are_featured()

    navbar = {
        'products': products,
        'categories': categories,
        'order': order,
        'latest': latest,
        'blogs': blogs,
        'popular_products': popular_products,
        'featured': featured,
    }

    if request.user.is_authenticated:
        try:
            order2 = Order.objects.get(user=request.user, ordered=False)
            if order2:
                navbar.update({'order2': order2})
        except ObjectDoesNotExist:
            pass
    return navbar
