from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
# Unnecessary, but saves us having to always pass in the settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swayola_api.settings')

# Create the celery instance
app = Celery('swayola_api')

# Configure celery from the django settings module
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks set up in separate tasks.py modules
app.autodiscover_tasks()

# Configure the cronjob schedule
app.conf.beat_schedule = {
    'write-vote-counts-to-db-every-minute': {
        'task': 'polls.tasks.write_vote_counts_to_db',
        'schedule': crontab(minute='*/1'),  # Change as per your requirement
    },
    # TODO: Run a greater vote count / sync cron job every week or so
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
