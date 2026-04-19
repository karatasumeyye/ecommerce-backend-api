from rest_framework.exceptions import ValidationError
from .models import Order, OrderItem
from carts.models import Cart, CartItem
from products.services import check_product_stock, decrease_product_stock
from django.db import transaction
from addresses.services import get_user_adress_or_404
from payments.services import create_payment
from coupons.services import get_valid_coupon_or_none

# ıf there is a error, don't save any changes

@transaction.atomic
def create_order_from_cart(user, cart):

@transaction.atomic
def create_order_from_cart(user, cart, delivery_address_id, billing_address_id, card_data, coupon_code=None):
    cart_items = cart.items.select_related("product").all()
    cart_items = cart.items.select_related("product").all()

    if not cart_items:
        raise ValidationError({'error': 'Your cart is empty.'})

    # Create the order record first
    delivery_address = get_user_adress_or_404(user, delivery_address_id)
    billing_address = get_user_adress_or_404(user, billing_address_id)

    coupon = get_valid_coupon_or_none(coupon_code)
        
    order = Order.objects.create(
        user=user, 
        delivery_address=delivery_address, 
        billing_address=billing_address,
        coupon = coupon
    )

    # Validate stock synchronously to provide immediate feedback
    for item in cart_items:
        check_product_stock(item.product, item.quantity)

        OrderItem.objects.create(
            order = order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

    order.calculate_total()
    cart.items.all().delete()

    # Enqueue asynchronous stock decrement after DB transaction commits
    def _enqueue_decrement():
        # Import inside closure to avoid circular imports at module import time
        from orders.tasks import decrement_stock_for_order

        decrement_stock_for_order.delay(order.id)   # Add the task to the Celery queue

    transaction.on_commit(_enqueue_decrement)

    payment_result = create_payment(user, order, card_data)

    cart.items.all().delete()

    return order, payment_result
      