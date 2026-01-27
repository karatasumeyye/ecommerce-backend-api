from rest_framework.exceptions import ValidationError
from .models import Order, OrderItem
from carts.models import Cart, CartItem
from products.services import check_product_stock, decrease_product_stock
from django.db import transaction
from addresses.services import get_user_adress_or_404
from payments.services import create_payment

# If paying is successful, create order and order items from cart item 
# If any step fails, the whole transaction is rolled back

@transaction.atomic  # Ensures atomicity of the order creation process  / ya yap ya da hiç yapma 
def create_order_from_cart(user, cart, delivery_address_id,billing_address_id, cart_data):

    cart_items = cart.items.select_related("product").all()  # Evert cart item with product details

    if not cart_items:
        raise ValidationError({"error": "Cart is empty."})
    
    delivery_address = get_user_adress_or_404(user, delivery_address_id)
    billing_address = get_user_adress_or_404(user, billing_address_id)
    
    order = Order.objects.create(user=user, delivery_address=delivery_address, billing_address=billing_address)

    for item in cart_items:
        check_product_stock(item.product, item.quantity)
        #decrease_product_stock(item.product, item.quantity)

        OrderItem.objects.create(
            order=order,
            product = item.product,
            quantity = item.quantity,
            price = item.product.price
        )

    order.calculate_total()

    payment_result = create_payment(user,order, cart_data)

    cart.items.all().delete()  # Clear cart after order creation

    return order,payment_result


