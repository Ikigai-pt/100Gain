from config import celeryconfig
from celery import Celery
APP_NAME = '100Gain'

try:
    app = Celery(APP_NAME)
    app.config_from_object(celeryconfig)
except ImportError:
    print ('celeryconfig not found')

