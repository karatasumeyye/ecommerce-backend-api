from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import OrderProductItemSerializer
from addresses.serializers import AddressDetailSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderProductItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    items = OrderItemSerializer(many=True, read_only=True)
    addresses = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
            "status",
            "total_price",
            "items",
            "addresses",

        ]
    def get_addresses(self,obj):
        return{
            'delivery_address': AddressDetailSerializer(obj.delivery_address).data if obj.delivery_address else None,
            'billing_address': AddressDetailSerializer(obj.billing_address).data if obj.billing_address else None,
        }


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']