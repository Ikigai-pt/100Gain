### how to execute
- DB
docker run --name sqlalchemy-orm-psql     -e POSTGRES_PASSWORD=dbpassword     -e POSTGRES_USER=dbuser     -e POSTGRES_DB=stock     -p 5432:5432     -d postgres

- Worker : open terminal `pipenv shell`
pipenv run celery -A stock.tasks.manageStock worker --loglevel=info

- Main app
pipenv run python -m stock.publisher.publishVolatileStocks


Running via celery beats
- Worker
celery -A App  worker --loglevel=info
- Schedular
celery -A App beat --loglevel=info
