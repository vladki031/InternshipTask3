from django.urls import path
from .views import ProductListAPI, ProductDetailAPI, OrderCreateAPI, UserOrderListAPI, home

urlpatterns = [
    path('products/', ProductListAPI.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailAPI.as_view(), name='product-detail'),
    path('orders/', OrderCreateAPI.as_view(), name='order-create'),
    path('user/orders/', UserOrderListAPI.as_view(), name='user-order-list'),
    path('', home, name='home'),
]
