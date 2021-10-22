
import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(logger_formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
#logger.propagate = False

def getLogger(name=None):
    return logging.getLogger(name)


import hashlib
def file_md5(filepath, buffer_size=4096):
    hash = hashlib.md5()
    with open(filepath, 'rb') as fp:
        for buf in iter(lambda: fp.read(buffer_size), b''):
            hash.update(buf)
    return hash
