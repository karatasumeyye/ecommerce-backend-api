from django.contrib import admin
from .models import Product,ProductImage

admin.site.register(Product)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product','id','alt_text')
    list_filter = ('product',)