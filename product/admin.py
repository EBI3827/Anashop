from django.contrib import admin
from .models import (Category, Subcategory, Product, Images,
                     Compare, CompareItem, Wishlist, WishItem, Contact, ProductComment, Hit)
# Register your models here.


class ProductImagesInline(admin.StackedInline):
    model = Images


class SubcategoryInline (admin.TabularInline):
    model = Subcategory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'subcategory', 'price', 'added_date']
    list_filter = ['added_date', 'category']
    list_editable = ['price', ]

    inlines = [ProductImagesInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    # prepopulated_fields = {'slug': ('title', )}
    inlines = [SubcategoryInline]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'product', 'parent', 'date', 'approved')
    list_editable = ('approved',)
    readonly_fields = ('date',)
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


admin.site.register(Compare)
admin.site.register(Wishlist)
admin.site.register(Contact)
admin.site.register(Hit)
