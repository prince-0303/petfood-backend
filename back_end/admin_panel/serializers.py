from rest_framework import serializers
from accounts.models import Register
from products.models import Product, Category
from orders.models import Order, OrderItem

# Dashboard
class DashboardStatsSerializer(serializers.Serializer):
    user_count = serializers.IntegerField()
    order_count = serializers.IntegerField()
    earnings = serializers.DecimalField(max_digits=10, decimal_places=2)
    users = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)

# User Management
class AdminUserSerializer(serializers.ModelSerializer):
    total_orders = serializers.SerializerMethodField()
    
    class Meta:
        model = Register
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'restricted', 'date_joined', 'total_orders']
    
    def get_total_orders(self, obj):
        return obj.orders.count()

# Category
class AdminCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# Product Management
class AdminProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'weight_value', 'weight_unit', 
                  'image_url', 'category', 'category_name', 'created_at']
        read_only_fields = ['id', 'created_at']

# Order Management
class AdminOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'price', 'quantity']

class AdminOrderSerializer(serializers.ModelSerializer):
    items = AdminOrderItemSerializer(many=True, read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'user_email', 'user_name', 'subtotal', 'tax', 'delivery', 
                  'total', 'status', 'placed_at', 'items']
        read_only_fields = ['id', 'placed_at']
    
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or "N/A"