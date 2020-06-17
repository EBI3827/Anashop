from django.contrib import admin
from .models import OrderItem, Order

# Register your models here.

admin.site.register(OrderItem)
admin.site.register(Order)
