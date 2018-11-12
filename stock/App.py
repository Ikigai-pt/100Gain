from config import celeryconfig
from celery import Celery
APP_NAME = 'stocks'

try:
    app = Celery(APP_NAME)
    app.config_from_object(celeryconfig)
except ImportError:
    print ('celeryconfig not found')

