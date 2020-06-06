from .models import Product,Category
def nav (request):
    products = Product.objects.all().order_by('-added_date')
    categories = Category.objects.all()
    navbar = {
        'products': products,
        'categories': categories,
    }
    return navbar