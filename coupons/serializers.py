from rest_framework import serializers
from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = [
            "id",
            "code",
            "discount_percent",
            "discount_amount",
            "start_date",
            "end_date",
            "active",
            "usage_limit",
            "usage_count",
        ]
        read_only_fields = ["usage_count"]

    def validate_code(self,value):
        if not value.strip():
            raise serializers.ValidationError("Coupon code cannot be empty or whitespace.")
        return value
    def validate_discount_percent(self, value):
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Discount percent must be between 0 and 100.")
        return value
    
    def validate_discount_amount(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Discount amount must be a positive value.")
        return value
    
    def validate_usage_limit(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("Usage limit must be a positive integer.")
        return value
    
    def validate(self, data):
        discount_percent = data.get("discount_percent")
        discount_amount = data.get("discount_amount")

        if self.instance and self.partial:
            discount_percent = discount_percent if discount_percent is not None else self.instance.discount_percent
            discount_amount = discount_amount if discount_amount is not None else self.instance.discount_amount

        if not discount_percent and not discount_amount:
            raise serializers.ValidationError("Either discount percent or discount amount must be provided.")
        
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("End date must be after start date.")
        
        return data

