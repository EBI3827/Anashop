from .models import Product,Category
from cart.models import Order
# from django.contrib import messages
# from django.core.exceptions import ObjectDoesNotExist
# from django.shortcuts import redirect


def nav (request):
   
    categories = Category.objects.all()
    order = request.GET.get('order', 'added_date')  # Set 'name' as a default value
    products = Product.objects.all().order_by(order)

    navbar = {
        'products': products,
        'categories': categories,
        'order':order
    }
    return navbar


# def get(request):
#     user = request.user
#     if user.is_authenticated():
#         try:
#             orders = Order.objects.filter(user=user, ordered=False)
#             if orders.exists():
#                 order = orders[0]
#                 return {'object': order}
#         except ObjectDoesNotExist:
#             return redirect("account_login")