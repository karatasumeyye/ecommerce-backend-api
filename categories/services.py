from .models import Category
from rest_framework.exceptions import NotFound


def get_category_or_404(category_id):
    try:
        return Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise NotFound("Category not found.")