from django.shortcuts import render,  redirect,get_object_or_404
from django.contrib import messages
from django.views.generic import DetailView, ListView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Subcategory, Compare, CompareItem, Wishlist, WishItem

# Create your views here.


def home(request):
    latest = Product.objects.all().order_by('-added_date')[:8]
    return render(request, 'index.html', {'latest': latest})


def productlist(request):
    latest = Product.objects.all().order_by('-added_date')[:8]
    return render(request, 'category.html', {'latest': latest})


def product_category(request,pk, slug):
    qs = Category.objects.get(id=pk, slug=slug)
    latest = Product.objects.all().order_by('-added_date')[:8]
    context = {
        'category': qs,
        'latest': latest,
    }
    return render(request, 'pcat.html', context)


def product_subcategory(request,category, pk, slug):
    qs = Subcategory.objects.get(id=pk)
    cqs = Category.objects.get(subcategory=qs)
    latest = Product.objects.all().order_by('-added_date')[:8]
    context = {
        'category': cqs,
        'subcategory': qs,
        'latest': latest,
    }
    return render(request, 'psub.html', context)


class ProductDetailView(DetailView):
    model = Product
    query_pk_and_slug = True
    template_name = 'product.html'


class CompareView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            compare = Compare.objects.get(
                user=self.request.user)
            context = {'object': compare}
            return render(self.request, 'compare.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have active order.')
            return redirect("/")

@login_required
def add_to_compare(request, pk):
    product = get_object_or_404(Product, id=pk)
    compare_item, created = CompareItem.objects.get_or_create(
        product=product,
        user=request.user,
    )
    compare_qs = Compare.objects.filter(user=request.user)
    if compare_qs.exists():
        compare = compare_qs[0]
        if compare.products.filter(product__id=product.id).exists():
            messages.info(request, 'This item quantity was updated.')
        else:
            compare.products.add(compare_item)
            messages.info(request, 'This item was added to your cart.')
            redirect('product:compare')
    else:
        compare = Compare.objects.create(user=request.user,
                                     )
        compare.products.add(compare_item)
        messages.info(request, 'This item was added to your cart.')
        return redirect('product:compare')
    return redirect('product:compare')

@login_required
def remove_from_compare(request, pk):
    product = get_object_or_404(Product, id=pk)
    order_qs = Compare.objects.filter(
        user=request.user,
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__id=product.id).exists():
            order_item = CompareItem.objects.filter(
                product=product,
                user=request.user,
            )[0]
            order.products.remove(order_item)
            order_item.delete()
            messages.warning(
                request, f"{order_item.product.name} از سبد خرید شما حذف شد !")
            return redirect('product:compare')
        else:
            messages.warning(request, "This item was not in your cart")
            return redirect('product:compare')
    else:
        messages.warning(request, "شما سفارش فعالی ندارید !")
        return redirect('product:compare')

class WishView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            wish = Wishlist.objects.get(
                user=self.request.user)
            context = {'object': wish}
            return render(self.request, 'wishlist.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have active order.')
            return redirect("/")

@login_required
def add_to_wishlist(request, pk):
    product = get_object_or_404(Product, id=pk)
    wish_item, created = WishItem.objects.get_or_create(
        product=product,
        user=request.user,
    )
    wish_qs = Wishlist.objects.filter(user=request.user)
    if wish_qs.exists():
        wish = wish_qs[0]
        if wish.products.filter(product__id=product.id).exists():
            messages.info(request, 'This item quantity was updated.')
        else:
            wish.products.add(wish_item)
            # messages.info(request, 'This item was added to your cart.')
            redirect('product:wishlist')
    else:
        wish = Wishlist.objects.create(user=request.user,
                                     )
        wish.products.add(wish_item)
        # messages.info(request, 'This item was added to your cart.')
        return redirect('product:wishlist')
    return redirect('product:wishlist')

@login_required
def remove_from_wishlist(request, pk):
    product = get_object_or_404(Product, id=pk)
    order_qs = Wishlist.objects.filter(
        user=request.user,
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__id=product.id).exists():
            order_item = WishItem.objects.filter(
                product=product,
                user=request.user,
            )[0]
            order.products.remove(order_item)
            order_item.delete()
            messages.warning(
                request, f"{order_item.product.name} از سبد خرید شما حذف شد !")
            return redirect('product:wishlist')
        else:
            messages.warning(request, "This item was not in your cart")
            return redirect('product:wishlist')
    else:
        messages.warning(request, "شما سفارش فعالی ندارید !")
        return redirect('product:wishlist')

def contact(request):
    return render(request, 'contact-us.html', {})

def checkout(request):
    return render(request, 'checkout.html', {})

def about_us(request):
    return render(request, 'about-us.html', {})

def compare(request):
    return render(request, 'compare.html', {})

def search(request):
    return render(request, 'search.html', {})

def wishlist(request):
    return render(request, 'wishlist.html', {})

def sitemap(request):
    return render(request, 'sitemap.html', {})

def handler404(request,exception):
    return render(request, '404.html', status=404)

# def handler500(request):
#     return render(request, '500.html', status=500)


