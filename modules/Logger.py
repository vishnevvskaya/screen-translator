import logging

logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]: %(message)s', 
                              datefmt='%d-%m-%y %H:%M:%S')

f_handler = logging.FileHandler('log.log', 'w', 'utf-8')
f_handler.setLevel(logging.DEBUG)
f_handler.setFormatter(formatter)

logger.addHandler(f_handler)