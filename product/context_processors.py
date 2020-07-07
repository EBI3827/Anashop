from .models import Product,Category
from cart.models import Order, OrderItem
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

def nav (request,*args, **kwargs):
    categories = Category.objects.all()
    order = request.GET.get('order', 'added_date')
    products = Product.objects.all().order_by(order)
    latest = Product.objects.all().order_by('-added_date')[:4]
    best_sell=Order.objects.filter(ordered=True)
    navbar = {
        'products': products,
        'categories': categories,
        'order':order,
        'latest': latest,
        'best_sell': best_sell,
    }

    if request.user.is_authenticated:
        try:
            order2 = Order.objects.get(user=request.user, ordered=False)
            if order2:
                navbar.update({'order2': order2})
        except ObjectDoesNotExist:
            pass
    return navbar