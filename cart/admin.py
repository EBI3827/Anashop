from django.contrib import admin
from .models import OrderItem, Order, Coupon,CheckoutInfo

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=('user','product','quantity', 'ordered')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('user', 'start_date','ordered_date','ordered')

# admin.site.register(OrderItem)
# admin.site.register(Order)
admin.site.register(Coupon)
admin.site.register(CheckoutInfo)


