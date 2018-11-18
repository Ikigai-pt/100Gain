### how to execute
- Worker : open terminal `pipenv shell`
pipenv run celery -A stock.tasks.recordVolatileStock worker --loglevel=info

- Main app
pipenv run python -m stock.publisher.publishVolatileStocks
