# http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'satellite_tracker.settings')
app = Celery('satellite_tracker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'update_database': {
        'task': 'starlink_code.functions.updateDB',
        'schedule': 7200.0
    },
    'update_starlink_position': {
        'task': 'starlink_code.functions.updateStarLink',
        'schedule': 9.0
    },
}
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
