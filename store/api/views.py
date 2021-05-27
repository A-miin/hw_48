# import json
#
# from django.http import JsonResponse
# from rest_framework.generics import get_object_or_404
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from online_store.models import Product
# from .serializers import ProductSerializer
#
#
# class ProductView(APIView):
#     def get(self, request, *args, **kwargs):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         response_data = serializer.data
#
#         return Response(data=response_data)
#
#     def post(self, request, *args, **kwargs):
#         product_data = request.data
#         serializer = ProductSerializer(data=product_data)
#         serializer.is_valid(raise_exception=True)
#         product = serializer.save()
#         return JsonResponse({'id': product.id})
#
#
# class ProductDetailUpdateDeleteView(APIView):
#     def put(self, request, *args, **kwargs):
#         product_id = self.kwargs.get('pk', 0)
#         instance = get_object_or_404(Product, id=product_id)
#         serializer = ProductSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data=serializer.data)
#
#     def get(self, request, *args, **kwargs):
#         product_id = self.kwargs.get('pk', 0)
#         instance = get_object_or_404(Product, id=product_id)
#         serializer = ProductSerializer(instance=instance)
#         return Response(data=serializer.data)
#
#     def delete(self, request, *args, **kwargs):
#         product_id = self.kwargs.get('pk', 0)
#         instance = get_object_or_404(Product, id=product_id)
#         instance.delete()
#         return Response(data={'id': product_id})
#
from rest_framework import viewsets
from online_store.models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer