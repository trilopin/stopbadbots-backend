
import logging
import logging.handlers

def setup_logger(params, logger=None):

    if logger is None:
        logger = logging.getLogger()

    logger.setLevel(params['level'])
    logger.propagate = False
    filehandler = logging.FileHandler(params['file'])
    filehandler.setFormatter(logging.Formatter(
        fmt='%(asctime)s %(levelname)s\t%(name)s\t%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'))
    logger.handlers = [filehandler]