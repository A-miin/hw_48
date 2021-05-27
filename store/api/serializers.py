from rest_framework import serializers

from online_store.models import Product, ProductOrder, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'category', 'remainder','price')
        read_only_fields = ('id',)


class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = ('id', 'order', 'product', 'qty')

class OrderSerializer(serializers.ModelSerializer):
    products = ProductOrderSerializer(many=True)
    class Meta:
        model = Order
        fields = ('user', 'name', 'tel', 'address','created_at', 'products')
