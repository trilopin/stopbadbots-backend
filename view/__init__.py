import importlib
from model.persistence import AerospikeSession


class BaseResource(object):
    '''
    Base resource class for views

        * inject config dict
        * force db keyspace to main keyspace
    '''
    def __init__(self, settings):
        self.settings = settings
        self.session = AerospikeSession(**settings['aerospike'])

    def _model(self, modulename, modelname):
        '''helper method for unit testing'''
        module = importlib.import_module(modulename)
        return getattr(module, modelname)

    def debug(self, msg):
        '''debug logging wrapper'''
        self.logger.debug(msg)

    def error(self, msg):
        '''error logging wrapper'''
        self.logger.error(msg)

    def info(self, msg):
        '''info logging wrapper'''
        self.logger.info(msg)

    def warning(self, msg):
        '''warning logging wrapper'''
        self.logger.warning(msg)