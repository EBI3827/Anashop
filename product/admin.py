from django.contrib import admin
from .models import Category, Subcategory, Product,Images,Compare,CompareItem,Wishlist,WishItem
# Register your models here.

class ProductImagesInline(admin.StackedInline):
    model = Images

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category','subcategory', 'price', 'added_date']
    list_filter = ['added_date', 'category']
    list_editable = ['price',]
    
    inlines = [ProductImagesInline]
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    # prepopulated_fields = {'slug': ('title', )}


# admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(Subcategory)
admin.site.register(CompareItem)
admin.site.register(Compare)
admin.site.register(Wishlist)
admin.site.register(WishItem)

