from os import environ

RABBITMQ_HOST = "otter.rmq.cloudamqp.com"
RABBITMQ_PORT = 5672
RABBITMQ_VHOST = "ripmimuk"
RABBITMQ_USER = "ripmimuk"
RABBITMQ_PASSWORD = "PH-MAv7gX2jwG9XkmGvFiPYpsFK4Jkn7"
BROKER_URL = environ.get('RABBITMQ_URL', "amqp://{user}:{password}@{host}:{port}/{vhost}".format(
    user=RABBITMQ_USER, password=RABBITMQ_PASSWORD, host=RABBITMQ_HOST, port=str(RABBITMQ_PORT), vhost=RABBITMQ_VHOST))

POSTGRESS_URL = 'postgresql://dbuser:dbpassword@localhost:5432/stock'
