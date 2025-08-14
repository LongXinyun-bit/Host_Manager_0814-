import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'host_manager.settings')

app = Celery('host_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# 确保测试环境直接本地执行
app.conf.task_always_eager = getattr(settings, 'CELERY_TASK_ALWAYS_EAGER', False)
app.conf.task_eager_propagates = getattr(settings, 'CELERY_TASK_EAGER_PROPAGATES', False) 