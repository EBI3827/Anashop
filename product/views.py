from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category

# Create your views here.


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'index.html', context)

def productlist (request):
    products = Product.objects.all()
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

