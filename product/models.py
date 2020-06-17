from django.db import models
from datetime import datetime  
from django.utils.text import slugify
from django.shortcuts import reverse
from django.conf import settings


# Create your models here.

LABEL_CHOICES = (
    ('موجود', 'موجود'),
    ('ناموجود', 'ناموجود'),
)

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True,blank=True, default='test', allow_unicode=True)

    def __str__(self):
        return self.title

    # def get_slug(self):
    #     return slugify(self.title)

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product:category', kwargs={ 'pk':self.id,'slug': self.slug })




class Subcategory(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,null=True, related_name='subcategory')
    slug = models.SlugField(null=True,blank=True, default='test', allow_unicode=True)

    def __str__(self):
        return self.title
    
    def get_category_slug(self):
        category_slug=slugify(self.category,allow_unicode=True)
        return category_slug

    def get_absolute_url(self):
        return reverse('product:subcategory', kwargs={'category':self.get_category_slug(), 'pk':self.id, 'slug': self.slug })

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)


class Product (models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    discount_price = models.IntegerField(null=True, blank=True)
    miniimage = models.ImageField(upload_to='products/', null=True, blank=True)
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE,null=True, related_name='products')
    label = models.CharField(choices=LABEL_CHOICES, default='M',max_length=8)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,null=True, related_name='products')
    added_date=models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True,blank=True, default='test', allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:product-detail', kwargs={'pk':self.id, 'slug': self.slug })

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)

    def save_percent(self):
        if self.discount_price:
            saving = int(((self.price - self.discount_price)/self.price) * 100)
            return saving
        return 0

    def get_label_color (self):
        if self.label=='موجود':
            return 'instock'
        else:
            return 'nostock'
    
    def featured(self):
        save=self.save_percent()
        if save >= 5 :
            return True
        else:
            return False

    def get_add_to_cart_url(self):
        return reverse('cart:add_to_cart', kwargs={'pk': self.id})

    def get_remove_from_cart_url(self):
        return reverse('cart:remove_from_cart', kwargs={'pk': self.id})

    def get_add_to_compare_url(self):
        return reverse('product:add_to_compare', kwargs={'pk': self.id})

    def get_remove_from_compare_url(self):
        return reverse('product:remove_from_compare', kwargs={'pk': self.id})

    def get_add_to_wishlist_url(self):
        return reverse('product:add_to_wishlist', kwargs={'pk': self.id})

    def get_remove_from_wishlist_url(self):
        return reverse('product:remove_from_wishlist', kwargs={'pk': self.id})

class Images (models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='images')
    miniimage = models.ImageField(upload_to='products/', blank=True)


class CompareItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

class Compare(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(CompareItem)

class WishItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(WishItem)


    def __str__(self):
        return self.user.username