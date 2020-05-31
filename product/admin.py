from django.contrib import admin
from .models import Category, Subcategory, Product
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Subcategory)