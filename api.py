import os
import sys
import json
import falcon
import mimetypes
from wsgiref import simple_server


from settings import settings
from logger import setup_logger
from middleware import RequireJSON
from middleware import JSONTranslator
from middleware import AuthMiddleware
from middleware import CrossAllowOrigin
from routing import generate_routes

# development: 'gunicorn api:app --reload'
# production: 'gunicorn -w3 --certfile=server.crt --keyfile=server.key api:app'
sys.path.append(os.path.abspath('.'))


setup_logger(settings['log'])

app = falcon.API(middleware=[
    CrossAllowOrigin(),
    RequireJSON(),
    JSONTranslator(),
    AuthMiddleware(settings),
])

generate_routes(app, settings)





