"""
Orders App - Celery Tasks

Task = Arka planda çalışacak görev

Kullanım:
    from orders.tasks import log_new_order
    log_new_order.delay(order_id)  # .delay() = "arka planda çalıştır"
"""

from celery import shared_task
import logging

# Logger oluştur
logger = logging.getLogger(__name__)

 
@shared_task
def log_new_order(order_id):
    """
    Yeni sipariş oluşturulduğunda arka planda çalışır.
    
    Bu basit bir örnek:
    - Sipariş bilgilerini loglar
    - İleride: email gönderme, stok güncelleme vb. eklenebilir
    
    Args:
        order_id: Siparişin ID'si
    """
    from orders.models import Order  # Circular import'u önlemek için içeride import
    
    try:
        order = Order.objects.get(id=order_id)
        
        # Sipariş bilgilerini logla
        logger.info(f"""
        ========================================
        YENİ SİPARİŞ OLUŞTURULDU (Arka planda işlendi)
        ========================================
        Sipariş ID: {order.id}
        Kullanıcı: {order.user.username}
        Toplam: {order.total_price}
        Durum: {order.status}
        Tarih: {order.created_at}
        ========================================
        """)
        
        return {
            'status': 'success',
            'order_id': order_id,
            'message': f'Sipariş #{order_id} başarıyla loglandı'
        }
        
    except Order.DoesNotExist:
        logger.error(f"Sipariş bulunamadı: #{order_id}")
        return {'status': 'error', 'message': f'Sipariş #{order_id} bulunamadı'}
    except Exception as e:
        logger.error(f"Hata oluştu: {e}")
        raise  # Celery'nin hatayı görmesi için tekrar fırlat


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def decrement_stock_for_order(self, order_id):
    """
    Decrement product stock for the given order.

    This task runs in the worker and uses a DB transaction + select_for_update
    to avoid simple race conditions. If any product has insufficient stock
    the order will be marked as 'cancelled'.
    """
    from django.db import transaction
    from orders.models import Order, OrderItem
    from products.models import Product
    import logging

    logger = logging.getLogger(__name__)

    try:
        with transaction.atomic():
            order = Order.objects.select_for_update().get(id=order_id)

            if order.status != 'pending':
                logger.info(f"Order #{order_id} not in pending state: {order.status}")
                return {'status': 'skipped', 'order_id': order_id, 'reason': 'not pending'}

            items = OrderItem.objects.filter(order=order).select_related('product')

            for item in items:
                product = Product.objects.select_for_update().get(id=item.product_id)
                if product.stock < item.quantity:
                    order.status = 'cancelled'
                    order.save(update_fields=['status'])
                    logger.warning(f"Order #{order_id} cancelled - insufficient stock for product #{product.id}")
                    return {'status': 'failed', 'order_id': order_id, 'reason': f'insufficient stock for {product.id}'}

                product.stock -= item.quantity
                product.save(update_fields=['stock'])

            order.status = 'processing'
            order.save(update_fields=['status'])

        logger.info(f"Stock decremented and order #{order_id} marked processing")
        return {'status': 'success', 'order_id': order_id}

    except Exception as exc:
        logger.exception(f"Error decrementing stock for order #{order_id}: {exc}")
        raise self.retry(exc=exc)
