from django.contrib import admin
from . import models


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image')
    search_fields = ('product__name',)
    list_filter = ('product',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'created_at','qr_code')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'created_at')
    ordering = ('-created_at',)

class EnterAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity','price', 'date')
    search_fields = ('product__name',)
    list_filter = ('date',)
    ordering = ('-date',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class OutlayAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'price','date', 'returned')
    search_fields = ('product__name',)
    list_filter = ('date', 'returned')
    ordering = ('-date',)


admin.site.register(models.ProductImage, ProductImageAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Enter, EnterAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Outlay, OutlayAdmin)
admin.site.register(models.Returned)