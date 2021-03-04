from django.urls import path

from .views import (
    index
)

urlpatterns = [
    path('', index, name='product_list'),  # URL для отображения списка productov
]
