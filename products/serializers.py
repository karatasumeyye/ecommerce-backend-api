from rest_framework import serializers
from .models import Product, ProductImage
from categories.models import Category
from rest_framework.validators import UniqueValidator
import re
from comments.serializers import CommentSerializer
from categories.serializers import CategorySerializer
from .services import validate_uploaded_image

class OrderProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = ['id','name','slug']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields = ['id','image','alt_text']
class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "stock", "slug", "category","images"]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "slug",
            "category",
            "comments",
        ]

class ProductSerializer(serializers.ModelSerializer):
    # Look like you started to define fields manually but then switched to ModelSerializer approach
    # id= serializers.IntegerField(read_only=True)
    # description=serializers.CharField(required=False, allow_blank=True, allow_null=True)
    # price=serializers.DecimalField(max_digits=10, decimal_places=2)
    # stock=serializers.IntegerField()
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    name = serializers.CharField(
        max_length=200, validators=[UniqueValidator(queryset=Product.objects.all())]
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        error_messages={
            "does_not_exist": "Category with the given ID does not exist.",
            "incorrect_type": "Invalid value. Category ID must be an integer.",
        },
    )

    # comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "stock", "slug", "category"]

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Product name must be at least 3 characters long."
            )
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be a positive number.")
        if value > 100000:
            raise serializers.ValidationError("Price seems too high.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value

    def validate_slug(self, value):
        if self.instance is None:
            if Product.objects.filter(slug=value).exists():
                raise serializers.ValidationError("Slug must be unique.")
        else:
            if Product.objects.filter(slug=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Slug must be unique.")

        if not re.match("^[a-z0-9]+(?:-[a-z0-9]+)*$", value):
            raise serializers.ValidationError(
                "Slug can only contain lowercase letters, numbers, and hyphens."
            )
        return value

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.stock = validated_data.get("stock", instance.stock)
        instance.save()
        return instance


class ProductImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields = ['image', 'alt_text']

    def validate_image(self,image):
        validate_uploaded_image(image)
        return image
