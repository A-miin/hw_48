from django.contrib import admin
from .models import Product, CartProduct
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'remainder']
    list_filter = ['name', 'price']
    search_fields = ['name', 'description']
    fields = ['id', 'name', 'description', 'category', 'remainder', 'price']
    readonly_fields = ['id']

class CartProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'qty']
    readonly_fields = ['id']

admin.site.register(Product, ProductAdmin)
admin.site.register(CartProduct, CartProductAdmin)