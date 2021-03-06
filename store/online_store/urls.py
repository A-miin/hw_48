from django.urls import path

from .views import (
    index,
    product_view,
    product_create,
)

urlpatterns = [
    path('', index, name='product_list'),  # URL для отображения списка productov
    path('product/<int:pk>/', product_view, name = 'product_view'),
    path('product/create', product_create, name = 'product_create'),
]
