from rest_framework.exceptions import ValidationError
from .models import Order, OrderItem
from carts.models import Cart, CartItem
from products.services import check_product_stock, decrease_product_stock
from django.db import transaction

@transaction.atomic  # Ensures atomicity of the order creation process  / ya yap ya da hiç yapma 
def create_order_from_cart(user, cart):

    cart_items = cart.items.select_related("product").all()  # Evert cart item with product details

    if not cart_items:
        raise ValidationError({"error": "Cart is empty."})
    
    order = Order.objects.create(user=user)

    for item in cart_items:
        check_product_stock(item.product, item.quantity)
        decrease_product_stock(item.product, item.quantity)

        OrderItem.objects.create(
            order=order,
            product = item.product,
            quantity = item.quantity,
            price = item.product.price
        )

    order.calculate_total()
    cart.items.all().delete()  # Clear cart after order creation

    return order


