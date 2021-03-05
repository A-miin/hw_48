from django.urls import path

from .views import (
    index,
    product_view
)

urlpatterns = [
    path('', index, name='product_list'),  # URL для отображения списка productov
    path('/product/<int:pk>/', product_view, name = 'product_view'),
]
