from django import template
from cart.models import OrderItem
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from product.models import Product

register = template.Library()


@register.simple_tag
def best_sell():
    sell = OrderItem.objects.filter(ordered=True).values(
        'product').annotate(sum=Sum('quantity')).order_by('-sum')[:6]
    best_sell = []
    for i in sell:
        id = i['product']
        p = get_object_or_404(Product, id=id)
        best_sell.append(p)
    return best_sell
