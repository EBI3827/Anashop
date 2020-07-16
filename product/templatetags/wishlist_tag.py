from django import template
from product.models import Wishlist

register = template.Library()


@register.filter
def wishlist_product_count(user):
    if user.is_authenticated:
        qs = Wishlist.objects.filter(user=user)
        if qs.exists():
            return qs[0].products.count()
    return 0
