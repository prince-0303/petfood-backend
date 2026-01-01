from django.urls import path
from .views import  DashboardView, UserManagementView, ProductManagementView, OrderManagementView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='admin-dashboard'),   
    path('users/', UserManagementView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserManagementView.as_view(), name='user-detail'),

    path('products/', ProductManagementView.as_view(), name='product-list'),
    path('products/<int:product_id>/', ProductManagementView.as_view(), name='product-detail'),

    path('orders/', OrderManagementView.as_view(), name='order-list'),
    path('orders/<int:order_id>/', OrderManagementView.as_view(), name='order-detail'),
]