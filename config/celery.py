# config/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# используем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('onetouch')

# загружаем настройки из settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# автопоиск задач в приложениях
app.autodiscover_tasks()
