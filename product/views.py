from django.shortcuts import render,  redirect, get_object_or_404, reverse, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import DetailView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.db.models import Q
from .forms import ContactForm, ProductCommentForm
from .decorators import check_recaptcha
from .models import (Product, Category, Subcategory, Compare,
                     CompareItem, Wishlist, WishItem, Contact, ProductComment, Hit)
import datetime
from django.contrib.contenttypes.models import ContentType
from hitcount.views import HitCountDetailView
# Create your views here.
from star_ratings.models import Rating


def render_to_response_hit_count(request, template_path, keys, response):
    for key in keys:
        for i in response[key]:
            Hit(content_object=i).save()
    return render(template_path, response)


def home(request):
    return render(request, 'index.html', {})


def productlist(request):
    order = request.GET.get('order')
    if order:
        products = Product.objects.all().order_by(order)
    else:
        products = Product.objects.all()
    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {
        'order': order,
        'page_obj': page_obj,
        'page_number': page_number
    }

    return render(request, 'category.html', context)


def product_category(request, pk, slug):
    qs = Category.objects.get(id=pk, slug=slug)
    order = request.GET.get('order')
    if order:
        pcategory = qs.products.all().order_by(order)
    else:
        pcategory = qs.products.all()
    paginator = Paginator(pcategory, 4)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {
        'order': order,
        'category': qs,
        'page_obj': page_obj,
        'page_number': page_number,
    }
    return render(request, 'pcat.html', context)


def product_subcategory(request, category, pk, slug):
    qs = Subcategory.objects.get(id=pk)
    cqs = Category.objects.get(subcategory=qs)
    order = request.GET.get('order')
    if order:
        pscategory = qs.products.all().order_by(order)
    else:
        pscategory = qs.products.all()
    paginator = Paginator(pscategory, 4)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {
        'category': cqs,
        'subcategory': qs,
        'page_obj': page_obj,
        'page_number': page_number,
        'order': order,
    }
    return render(request, 'psub.html', context)


class ProductDetailView(FormMixin, HitCountDetailView):
    model = Product
    query_pk_and_slug = True
    template_name = 'product.html'
    form_class = ProductCommentForm
    count_hit = True

    def get_success_url(self):
        return reverse('product:product-detail', kwargs={'pk': self.object.id, 'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['form'] = ProductCommentForm(initial={'product': self.object})
        context['comments'] = self.object.comments.filter(
            approved=True, parent=None).order_by('-date')
        context['rating'] = Rating.objects.get(
            object_id=self.object.id)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = ProductComment.objects.get(id=parent_id)
                replay_comment = form.save(commit=False)
                # assign parent_obj to replay comment
                replay_comment.parent = parent_obj
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(ProductDetailView, self).form_valid(form)


class CompareView(View):
    def get(self, *args, **kwargs):
        try:
            compare = Compare.objects.get(
                user=self.request.user)
            context = {'object': compare}
            return render(self.request, 'compare.html', context)
        except ObjectDoesNotExist:
            messages.error(
                self.request, 'شما محصولی در لیست مقایسه خود ندارید .')
            return redirect(self.request.META.get('HTTP_REFERER'))


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
            pass
        else:
            compare.products.add(compare_item)
            messages.info(
                request, f'{compare_item.product.name} به لیست مقایسه افزوده شد .')
            redirect(request.META.get('HTTP_REFERER'))
    else:
        compare = Compare.objects.create(user=request.user,
                                         )
        compare.products.add(compare_item)
        messages.info(
            request, f'{compare_item.product.name} به لیست مقایسه افزوده شد .')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


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
                request, f"{order_item.product.name} از لیست مقایسه شما حذف شد !")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(
                request,  f"{order_item.product.name} از لیست مقایسه شما حذف شد !")
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, "شما محصولی در لیست مقایسه خود ندارید .")
        return redirect(request.META.get('HTTP_REFERER'))


class WishView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            wish = Wishlist.objects.get(
                user=self.request.user)
            context = {'object': wish}
            return render(self.request, 'wishlist.html', context)
        except ObjectDoesNotExist:
            messages.error(
                self.request, 'شما محصولی در لیست علاقه مندی خود ندارید .')
            return redirect(self.request.META.get('HTTP_REFERER'))


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
            pass
        else:
            wish.products.add(wish_item)
            messages.info(
                request, f'{wish_item.product.name} به لیست علاقه مندی ها افزوده شد .')
            redirect(request.META.get('HTTP_REFERER'))
    else:
        wish = Wishlist.objects.create(user=request.user,
                                       )
        wish.products.add(wish_item)
        messages.info(
            request, f'{wish_item.product.name} به لیست علاقه مندی ها افزوده شد .')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


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
                request, f"{order_item.product.name} از لیست علاقه مندی های شما حذف شد !")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(
                request, f"{order_item.product.name} از لیست علاقه مندی های شما حذف شد !")
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, 'شما محصولی در لیست علاقه مندی خود ندارید .')
        return redirect(request.META.get('HTTP_REFERER'))


@check_recaptcha
def contact(request):
    if request.method == "POST":
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid() and request.recaptcha_is_valid:
            contact_form.save()
            # contact=Contact()
            # contact.name=request.POST.get('name')
            # contact.email=request.POST.get('email')
            # contact.message=request.POST.get('message')
            # contact.save()
            return redirect('product:contact-us')
        # else:
        #     print contact_form.errors
    else:
        contact_form = ContactForm()
    return render(request, 'contact-us.html', {"form": contact_form})


def about_us(request):
    return render(request, 'about-us.html', {})


def search(request):
    query = request.GET.get('q')
    cq = request.GET.get('category_title')
    order = request.GET.get('order')
    if cq:
        try:
            cat = Category.objects.get(title=cq)
            if order:
                result = Product.objects.filter(
                    Q(category=cat), Q(name__icontains=query)).order_by(order)
            else:
                result = Product.objects.filter(
                    Q(category=cat), Q(name__icontains=query))
            paginator = Paginator(result, 4)
            page_number = request.GET.get('page')
            try:
                results = paginator.page(page_number)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)
            context = {
                'order': order,
                'search_result': results,
                'query': query,
                'current_title': cq
            }
            return render(request, 'search.html', context)
        except ObjectDoesNotExist:
            if order:
                result = Product.objects.filter(
                    Q(name__icontains=query)).order_by(order)
            else:
                result = Product.objects.filter(Q(name__icontains=query))
            paginator = Paginator(result, 4)
            page_number = request.GET.get('page')
            try:
                results = paginator.page(page_number)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)
            context = {
                'order': order,
                'search_result': results,
                'query': query,
                'current_title': cq
            }
            return render(request, 'search.html', context)
    else:
        if order:
            result = Product.objects.all().order_by(order)
        else:
            result = Product.objects.all()
        paginator = Paginator(result, 4)
        page_number = request.GET.get('page')
        try:
            results = paginator.page(page_number)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        context = {
            'order': order,
            'search_result': results,
            'page_number': page_number,
        }
    return render(request, 'search.html', context)


def sitemap(request):
    return render(request, 'sitemap.html', {})


def faq(request):
    return render(request, 'faq.html', {})


def handler404(request, exception):
    return render(request, '404.html', status=404)
