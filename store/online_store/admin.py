from django.contrib import admin
from .models import Product
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price','category']
    list_filter = ['name', 'price']
    search_fields = ['name', 'description']
    fields = ['id', 'name', 'description', 'category', 'remainder', 'price']
    readonly_fields = ['id']

admin.site.register(Product, ProductAdmin)