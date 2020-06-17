from django import template
from product.models import Compare

register=template.Library()

@register.filter
def compare_product_count(user):
    if user.is_authenticated:
        qs=Compare.objects.filter(user=user)
        if qs.exists():
            return qs[0].products.count()
    return 0