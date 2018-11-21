from os import environ
from datetime import timedelta
from celery.schedules import crontab
RABBITMQ_HOST = "otter.rmq.cloudamqp.com"
RABBITMQ_PORT = 5672
RABBITMQ_VHOST = "fpppgeup"
RABBITMQ_USER = "fpppgeup"
RABBITMQ_PASSWORD = "5q_51aGeHwySwn1q6V88sD3jKuEIBRFV"
BROKER_URL = environ.get('RABBITMQ_URL', "amqp://{user}:{password}@{host}:{port}/{vhost}".format(
    user=RABBITMQ_USER, password=RABBITMQ_PASSWORD, host=RABBITMQ_HOST, port=str(RABBITMQ_PORT), vhost=RABBITMQ_VHOST))

POSTGRESS_URL = 'postgresql://dbuser:dbpassword@localhost:5432/stock'
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
CELERYBEAT_SCHEDULE = {
    "gather_volatile_stocks": {
        "task": "stock.tasks.manageStock.publishVolatileStock",
        'schedule': crontab(minute="*/2", hour="*"),
        'args': ()
    },
    "classify_stocks": {
        "task": "stock.tasks.manageStock.classifyStocks",
        'schedule': crontab(minute="0", hour="6-17/1", day_of_week="mon-fri"),
        'args': ()
    },
}
CELERY_IMPORTS = ['stock.tasks.manageStock']
MARKET_CLOSED_DATES = ['2018-11-22', '2018-12-25']
