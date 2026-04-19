"""
Django başladığında Celery'nin yüklenmesini sağlar.

Bu satırlar sayesinde:
- Django her başladığında Celery app aktif olur
- @shared_task decorator'ı kullanılabilir hale gelir
"""

from .celery import app as celery_app

# Bu değişkeni dışarı açıyoruz
__all__ = ('celery_app',)
