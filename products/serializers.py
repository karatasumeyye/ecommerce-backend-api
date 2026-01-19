from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    id= serializers.IntegerField(read_only=True)
    name=serializers.CharField(max_length=200)
    description=serializers.CharField(allow_blank=True)
    price=serializers.DecimalField(max_digits=10, decimal_places=2)
    stock=serializers.IntegerField()

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
    
    def update(self, instance,validated_data):
        instance.name= validated_data.get('name', instance.name)
        instance.description= validated_data.get('description', instance.description)
        instance.price= validated_data.get('price', instance.price)
        instance.stock= validated_data.get('stock', instance.stock)
        instance.save()
        return instance