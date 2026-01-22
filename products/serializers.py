from rest_framework import serializers
from .models import Product
from categories.models import Category
from rest_framework.validators import UniqueValidator
import re

class ProductSerializer(serializers.Serializer):
    id= serializers.IntegerField(read_only=True)
    name=serializers.CharField(max_length=200, validators=[UniqueValidator(queryset=Product.objects.all())])
    description=serializers.CharField(required=False, allow_blank=True, allow_null=True)
    price=serializers.DecimalField(max_digits=10, decimal_places=2)
    stock=serializers.IntegerField()
    slug=serializers.SlugField(validators= [UniqueValidator(queryset=Product.objects.all())])
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    def validate_name(self,value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Product name must be at least 3 characters long.")
        return value
    def validate_price(self,value):
        if value < 0:
            raise serializers.ValidationError("Price must be a positive number.")
        if value >100000:
            raise serializers.ValidationError("Price seems too high.")
        return value
    def validate_stock(self,value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value
    def validate_slug(self,value):
        if not re.match('^[a-z0-9]+(?:-[a-z0-9]+)*$', value):
            raise serializers.ValidationError("Slug can only contain lowercase letters, numbers, and hyphens.")
        return value



    def create(self, validated_data):
        return Product.objects.create(**validated_data)
    
    def update(self, instance,validated_data):
        instance.name= validated_data.get('name', instance.name)
        instance.description= validated_data.get('description', instance.description)
        instance.price= validated_data.get('price', instance.price)
        instance.stock= validated_data.get('stock', instance.stock)
        instance.save()
        return instance