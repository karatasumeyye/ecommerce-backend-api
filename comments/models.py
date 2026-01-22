from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product
class Comment(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(blank=True, null=True, max_length=200)
    active = models.BooleanField(default=True)
    creates= models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return str(self.rating) + "|" +self.product.name
