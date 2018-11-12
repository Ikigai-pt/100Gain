### how to execute
- Worker : open terminal
pipenv run celery -A stock.tasks.get_stock worker --loglevel=info

- Main app
pipenv run python -m stock.stockGatherer
