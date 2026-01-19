from rest_framework import serializers 
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id","rating","description","active","creates","update","product"]
        # Make the product field write-only to prevent it from being displayed in the API response
        extra_kwargs = {
            'product': {'write_only': True}
        }