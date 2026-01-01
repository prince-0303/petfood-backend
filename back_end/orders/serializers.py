from rest_framework import serializers
from .models import Address, Order, OrderItem

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ['user']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.CharField(source='product.image', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address_details = AddressSerializer(source='address', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'address', 'address_details', 'subtotal', 'tax', 'delivery', 'total', 'status', 'placed_at', 'items']
        read_only_fields = ['id', 'user', 'status', 'placed_at']

class CreateOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['address', 'subtotal', 'tax', 'delivery', 'total', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        request = self.context.get('request')
        
        order = Order.objects.create(
            user=request.user,
            status='Confirmed',
            **validated_data
        )
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order