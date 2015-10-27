#stopbadbot-backend

WIP - DO NOT USE (YET)


## development

gunicorn api:app --reload
celery -A tasks worker -l info  -f ../log/celery.log

## production

gunicorn -w3 --certfile=server.crt --keyfile=server.key api:app
celery -A tasks worker -l info  -f ../log/celery.log
