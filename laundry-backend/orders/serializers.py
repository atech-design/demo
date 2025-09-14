from rest_framework import serializers
from .models import Order, OrderItem
from catalog.serializers import ServiceSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "service", "qty", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "status", "total", "created_at", "items"]


