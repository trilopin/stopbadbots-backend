#stopbadbot-backend

WIP - DO NOT USE (YET)


### development
```
gunicorn api:app --reload --log-level debug
celery -A tasks worker -l debug  
```

### production

```
gunicorn -w3 --certfile=server.crt --keyfile=server.key api:app
celery -A tasks worker -l info  -f ../log/celery.log
```
