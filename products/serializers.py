from rest_framework import serializers
from .models import Product
from categories.models import Category
from rest_framework.validators import UniqueValidator
import re
from comments.serializers import CommentSerializer

class ProductSerializer(serializers.ModelSerializer):
    # Look like you started to define fields manually but then switched to ModelSerializer approach
    # id= serializers.IntegerField(read_only=True)
    # description=serializers.CharField(required=False, allow_blank=True, allow_null=True)
    # price=serializers.DecimalField(max_digits=10, decimal_places=2)
    # stock=serializers.IntegerField()
    #category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    
    name=serializers.CharField(max_length=200, validators=[UniqueValidator(queryset=Product.objects.all())])
    slug=serializers.SlugField(validators= [UniqueValidator(queryset=Product.objects.all())])
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model=Product
        fields = ["id","name","description","price","stock","slug","category","comments"]
    
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