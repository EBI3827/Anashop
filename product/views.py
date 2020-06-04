from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category

# Create your views here.


def home(request):
    products = Product.objects.all().order_by('-added_date')
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'index.html', context)

def productlist (request):
    products = Product.objects.all().order_by('-added_date')
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'category.html', context)

# class ProductListView(ListView):
#     model = [Product,Category]
#     template_name = 'category.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'

def contact(request):
    return render(request, 'contact-us.html', {})

def product_category(request, pk):
    qs=Category.objects.get(id=pk)
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'category': qs,
        'products': products,
        'categories': categories,
    }
    return render(request, 'pcat.html', context)

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