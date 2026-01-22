from rest_framework import serializers 
from .models import Comment
from users.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    #user = UserSerializer(read_only=True)  # Nested serializer to display user details
    #user = serializers.SlugRelatedField(read_only=True, slug_field='username')  # Display username only
    user = serializers.SerializerMethodField()  # Custom method field to get username
    class Meta:
        model = Comment
        fields = ["id","rating","description","active","creates","update","product","user"]
        # Make the product field write-only to prevent it from being displayed in the API response
        extra_kwargs = {
            'product': {'write_only': True,
                        "required": False},
            
        }

    def get_user(self,obj):
        return obj.user.username if obj.user else None