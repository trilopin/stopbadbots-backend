import sys
import os
from celery import Celery
from settings import settings

sys.path.append(os.path.abspath('.'))



# celery setup
celery_app = Celery('stopbadbots',
                    broker=settings['celery']['broker_url'],
                    backend=settings['celery']['backend_url'])
