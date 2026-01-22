from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email","username"]




class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required= True, validators=[validate_password])
    password2 = serializers.CharField(write_only = True, required= True)

    class Meta:
        model = User
        fields = ("id","email","phone","password","password2","first_name","last_name")

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password fields didn't match."})
        return attrs
    
    def create(self,validated_data):
        validated_data.pop('password2') # Remove password2 as it's not needed for user creation
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)  # Create a token for the new user
        return user