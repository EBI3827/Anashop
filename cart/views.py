from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.contrib import messages
from django.utils import timezone
from .models import OrderItem, Order, Coupon, CheckoutInfo
from product.models import Product
from .forms import CouponForm, CheckoutForm
import datetime

# Create your views here.


class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order': order,
                'couponform': CouponForm(),
                'DISPLAY_COUPON_FORM': True,
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'شما سفارش فعالی ندارید !')
            return redirect(self.request.META.get('HTTP_REFERER'))


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    if product.label == "موجود":
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
                messages.info(
                    request, f'{order_item.product.name} بروزرسانی شد .')
            else:
                order.products.add(order_item)
                messages.info(
                    request, f'{order_item.product.name} به سبد خرید شما افزوده شد .')
                redirect(request.META.get('HTTP_REFERER'))
        else:
            oredered_date = timezone.now()
            order = Order.objects.create(user=request.user,
                                         ordered_date=oredered_date)
            order.products.add(order_item)
            messages.info(
                request, f'{order_item.product.name} به سبد خرید شما افزوده شد .')
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


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
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "This item was not in your cart")
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, "شما سفارش فعالی ندارید !")
        return redirect(request.META.get('HTTP_REFERER'))


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


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        return redirect("cart:cart")


class AddCouponView (View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user,
                    ordered=False,
                )
                try:
                    order.coupon = get_coupon(self.request, code)
                    order.save()
                    messages.info(
                        self.request, "کد تخفیف با موفقیت اعمال شد !")
                    return redirect("cart:cart")
                except:
                    messages.success(self.request, "این کد تخفیف نامعتبر است.")
                    return redirect("cart:cart")
            except ObjectDoesNotExist:
                messages.success(self.request, "شما سفارش فعالی ندارید !")
                return redirect("cart:cart")


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'couponform': CouponForm(),
                'form': form,
                'DISPLAY_COUPON_FORM': False
            }

            checkoutinfo_qs = CheckoutInfo.objects.filter(
                user=self.request.user,
                default=True
            )
            if checkoutinfo_qs.exists():
                context.update(
                    {'default_info': checkoutinfo_qs[0]})
            return render(self.request, 'checkout.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "شما سفارش فعالی ندارید .")
            return redirect(self.request.META.get('HTTP_REFERER'))

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            try:
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                use_default_info = form.cleaned_data.get('use_default_info')
                if use_default_info:
                    info_qs = CheckoutInfo.objects.filter(
                        user=self.request.user,
                        default=True
                    )
                    if info_qs.exists():
                        info = info_qs[0]
                        order.checkoutinfo = info
                        order.save()
                    else:
                        messages.info(
                            self.request, "اطلاعات پیش فرضی وجود ندارد .")
                        return redirect('cart:checkout')
                else:
                    first_name = form.cleaned_data.get(
                        'first_name')
                    last_name = form.cleaned_data.get(
                        'last_name')
                    email = form.cleaned_data.get(
                        'email')
                    phone = form.cleaned_data.get('phone')
                    address = form.cleaned_data.get('address')
                    postal_code = form.cleaned_data.get('postal_code')

                    if is_valid_form([first_name, last_name, email, phone, address, postal_code]):
                        info = CheckoutInfo(
                            user=self.request.user,
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            phone=phone,
                            address=address,
                            postal_code=postal_code,
                        )
                        info.save()
                        order.checkoutinfo = info
                        order.save()

                        set_default_info = form.cleaned_data.get(
                            'set_default_info')
                        if set_default_info:
                            info.default = True
                            info.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")
                        return redirect("cart:checkout")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'DE':
                    return redirect('cart:payment', payment_option='پرداخت در محل')
                elif payment_option == 'CH':
                    return redirect('cart:payment', payment_option='واریز به حساب')
                elif payment_option == 'ZA':
                    return redirect('cart:payment', payment_option='زرین پال')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('cart:checkout')
            except ObjectDoesNotExist:
                messages.warning(self.request, "شما سفارش فعالی ندارید")
                return redirect(self.request.META.get('HTTP_REFERER'))
        else:
            return render(self.request, 'checkout.html', context={'form': form})


class PaymentView (View):

    def get(self, *args, **kwargs):
        return render(self.request, 'payment.html', {})

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)

        order_items = order.products.all()
        order_items.update(ordered=True)
        for item in order_items:
            item.save()

        order.ordered = True
        order.ordered_date = datetime.datetime.now()
        order.save()

        messages.success(self.request, "سفارش شما با موفیقت ثبت شد !")
        return redirect("/")
