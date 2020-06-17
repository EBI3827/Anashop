from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.views.generic import View
from .models import OrderItem, Order
from product.models import Product

# Create your views here.


class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {'object': order}
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'شما سفارش فعالی ندارید !')
            return redirect("/")


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    if product.label == "موجود" :
        order_item, created = OrderItem.objects.get_or_create(
            product=product,
            user=request.user,
            ordered=False,
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.products.filter(product__id=product.id).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f'{order_item.product.name} بروزرسانی شد .')
            else:
                order.products.add(order_item)
                messages.info(
                    request, f'{order_item.product.name} به سبد خرید شما افزوده شد .')
                redirect('cart:cart')
        else:
            oredered_date = timezone.now()
            order = Order.objects.create(user=request.user,
                                        ordered_date=oredered_date)
            order.products.add(order_item)
            messages.info(
                request, f'{order_item.product.name} به سبد خرید شما افزوده شد .')
            return redirect('cart:cart')
        return redirect('cart:cart')
    else:
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('cart:cart')


@login_required
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__id=product.id).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False,
            )[0]
            order.products.remove(order_item)
            order_item.delete()
            messages.warning(
                request, f"{order_item.product.name} از سبد خرید شما حذف شد !")
            return redirect('cart:cart')
        else:
            messages.warning(request, "This item was not in your cart")
            return redirect('cart:cart')
    else:
        messages.warning(request, "شما سفارش فعالی ندارید !")
        return redirect('cart:cart')


@login_required
def remove_single_item_from_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__id=product.id).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False,
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.products.remove(order_item)
                order_item.delete()
            messages.warning(
                request, f'{order_item.product.name} بروزرسانی شد .')
            return redirect('cart:cart')
        else:
            messages.warning(request, 'This item was not in your cart.')
            return redirect('cart:cart')
    else:
        messages.warning(request, "شما سفارش فعالی ندارید !")
        return redirect('/')
