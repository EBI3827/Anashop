from django.db import models
from datetime import datetime  

# Create your models here.

LABEL_CHOICES = (
    ('موجود', 'موجود'),
    ('ناموجود', 'ناموجود'),
)

class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,null=True, related_name='subcategory')

    def __str__(self):
        return self.title


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

    def __str__(self):
        return self.name

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
    