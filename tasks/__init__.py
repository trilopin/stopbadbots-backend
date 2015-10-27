from tasks.chunk import Chunk
from tasks.filetodb import FileToDb
from tasks.simplestats import SimpleStats
from tasks.outlierdetector import OutlierDetector
from celery_app import celery_app
from celery.utils.log import get_task_logger


@celery_app.task
def chunk(*args, **kwargs):
    kwargs['logger'] = get_task_logger('tasks.' + __name__)
    kwargs['process_file'] = filetodb
    kwargs['simple_stats'] = simple_stats
    chunker = Chunk(*args, **kwargs)
    return chunker.run()


@celery_app.task
def filetodb(*args, **kwargs):
    kwargs['logger'] = get_task_logger('tasks.' + __name__)
    filetodb = FileToDb(*args, **kwargs)
    return filetodb.run()


@celery_app.task
def simple_stats(*args, **kwargs):
    kwargs['logger'] = get_task_logger('tasks.' + __name__)
    kwargs['page_size'] = 10000
    simplestats = SimpleStats(*args, **kwargs)
    return simplestats.run()


@celery_app.task
def outlier_detector(*args, **kwargs):
    kwargs['logger'] = get_task_logger('tasks.' + __name__)
    outlierdetector = OutlierDetector(*args, **kwargs)
    return outlierdetector.run()
    return True
