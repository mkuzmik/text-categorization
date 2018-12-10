import logging
from config import CONFIG

formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
logging_level = CONFIG.LOGGING_LEVEL


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)
    ch = logging.StreamHandler()
    ch.setLevel(logging_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
