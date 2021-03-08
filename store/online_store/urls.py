from django.urls import path

from .views import (
    index,
    product_view,
    product_create,
    product_update,
    product_delete,
    product_category_list,
)

urlpatterns = [
    path('', index, name='product_list'),  # URL для отображения списка productov
    path('<category>', product_category_list, name='product_category_list'),  # URL для отображения списка productov
    path('product/<int:pk>/', product_view, name = 'product_view'),
    path('product/create', product_create, name = 'product_create'),
    path('product/<int:pk>/update', product_update, name = 'product_update'),
    path('product/<int:pk>/delete', product_delete, name = 'product_delete'),
]
