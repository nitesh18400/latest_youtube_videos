import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'latest_youtube_videos.settings')

app = Celery('latest_youtube_videos')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
