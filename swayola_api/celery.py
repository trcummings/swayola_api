from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('your_project')

# Using a string here means the worker will not have to pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Configure the cronjob schedule
app.conf.beat_schedule = {
    'write-vote-counts-to-db-every-minute': {
        'task': 'your_app.tasks.write_vote_counts_to_db',
        'schedule': crontab(minute='*/1'),  # Change as per your requirement
    },
    # TODO: Run a greater vote count / sync cron job every week or so
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
