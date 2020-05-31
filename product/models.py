from django.db import models

# Create your models here.


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
        Subcategory, on_delete=models.CASCADE,null=True, related_name='product')

    def __str__(self):
        return self.name

    def save_percent(self):
        if self.discount_price:
            saving = int(((self.price - self.discount_price)/self.price) * 100)
            return saving
        return 0
