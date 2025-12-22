from rest_framework import serializers
from .models import Address, Order, OrderItem

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ['user']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta :
        model = OrderItem
        fields = ['products','price','quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True)
    class Meta :
        model = Order
        fields = ['id', 'address', 'subtotal', 'tax', 'delivery', 'total', 'status', 'placed_at', 'items']
        read_only_fields = ['id', 'user', 'status', 'placed_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order

            