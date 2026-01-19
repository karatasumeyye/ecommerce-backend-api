from rest_framework import serializers
from .models import Category
from rest_framework.validators import UniqueValidator

class CategorySerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name= serializers.CharField(max_length=100,validators=[UniqueValidator(queryset=Category.objects.all())])
    description = serializers.CharField(required=False, allow_blank=True,allow_null=True)

    def validate(self,data):
        if data["name"] == data["description"]:
            raise serializers.ValidationError("Category name and description cannot be the same.") 
        else:
            return data

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Category name must be at least 3 characters long.")

    
        # if Category.objects.filter(name=value).exists():
        #     raise serializers.ValidationError("Category with this name already exists.")    
      
        return value

        
    def create(self, validated_data):
        return Category.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance