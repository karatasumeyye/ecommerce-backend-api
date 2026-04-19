"""
Celery Yapılandırması

Bu dosya:
1. Celery uygulamasını oluşturur
2. Django settings'ten ayarları okur
3. Tüm app'lerdeki tasks.py dosyalarını otomatik bulur
"""

import os
from celery import Celery

# Django settings modülünü belirt
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Celery uygulamasını oluştur
# 'config' = proje adı (config klasörü)
app = Celery('config')

# Django settings'ten CELERY_ ile başlayan ayarları oku
# Örnek: CELERY_BROKER_URL → broker_url olarak kullanılır
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tüm Django app'lerindeki tasks.py dosyalarını otomatik bul
# orders/tasks.py, products/tasks.py gibi dosyalar otomatik yüklenir
app.autodiscover_tasks()


# Debug için basit bir test görevi
@app.task(bind=True)
def debug_task(self):
    """Celery'nin çalıştığını test etmek için"""
    print(f'Celery çalışıyor! Request: {self.request!r}')
