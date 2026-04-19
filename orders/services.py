from rest_framework.exceptions import ValidationError
from .models import Order, OrderItem
from carts.models import Cart, CartItem
from products.services import check_product_stock
from django.db import transaction


@transaction.atomic
def create_order_from_cart(user, cart):

    cart_items = cart.items.select_related("product").all()

    if not cart_items:
        raise ValidationError({"error": "Cart is empty."})

    # Create the order record first
    order = Order.objects.create(user=user)

    # Validate stock synchronously to provide immediate feedback
    for item in cart_items:
        check_product_stock(item.product, item.quantity)

        OrderItem.objects.create(
            order=order,
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

    return order


