from django.urls import path

from .views import (
    IndexProductView,
    ViewProductView,
    CreateProductView,
    UpdateProductView,
    DeleteProductView,
    AddToCartView,
    IndexCartView,
    DeleteCartView,
    CreateOrderView,
    UserOrderView,
    StatView,
)
# app_name = 'store'
urlpatterns = [
    path('', IndexProductView.as_view(), name='product_list'),  # URL для отображения списка productov
    path('<category>', IndexProductView.as_view(), name='product_category_list'),  # URL для отображения списка productov
    path('product/<int:pk>/', ViewProductView.as_view(), name = 'product_view'),
    path('product/create', CreateProductView.as_view(), name = 'product_create'),
    path('product/<int:pk>/update', UpdateProductView.as_view(), name = 'product_update'),
    path('product/<int:pk>/delete', DeleteProductView.as_view(), name = 'product_delete'),
    path('basket/<int:pk>/add',AddToCartView.as_view(), name="add_to_cart"),
    path('basket/', IndexCartView.as_view(), name='cart_list'),
    path('basket/<int:pk>/delete', DeleteCartView.as_view(), name='cart-delete'),
    path('order/new',CreateOrderView.as_view(), name='order_create'),
    # path('user/order/new',CreateUserOrderView.as_view(), name='user_order_create'),
    path('user/orders',UserOrderView.as_view(), name='user_order_list'),
    path('stat/',StatView.as_view(), name='stat'),

]
