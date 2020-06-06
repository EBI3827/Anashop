from django.shortcuts import render
from django.views.generic import DetailView
from .models import Product, Category,Subcategory

# Create your views here.


def home(request):
    latest=Product.objects.all().order_by('-added_date')[:8]
    return render(request, 'index.html', {'latest' : latest})

def productlist (request):
    latest=Product.objects.all().order_by('-added_date')[:8]
    return render(request, 'category.html', {'latest' : latest})

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'

def contact(request):
    return render(request, 'contact-us.html', {})

def product_category(request, pk):
    qs=Category.objects.get(id=pk)
    latest=Product.objects.all().order_by('-added_date')[:8]
    context = {
        'category': qs,
        'latest' : latest,
    }
    return render(request, 'pcat.html', context)

def product_subcategory(request, pk):
    qs=Subcategory.objects.get(id=pk)
    cqs=Category.objects.get(subcategory=qs)
    latest=Product.objects.all().order_by('-added_date')[:8]
    context = {
        'category': cqs,
        'subcategory': qs,
        'latest' : latest,
    }
    return render(request, 'psub.html', context)

def checkout(request):
    return render(request, 'checkout.html', {})

def cart(request):
    return render(request, 'cart.html', {})

def about_us(request):
    return render(request, 'about-us.html', {})

def compare(request):
    return render(request, 'compare.html', {})

def search(request):
    return render(request, 'search.html', {})

def wishlist(request):
    return render(request, 'wishlist.html', {})