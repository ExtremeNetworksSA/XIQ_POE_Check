#!/usr/bin/env python3
import logging
import os
import time #TODO - Remove
import inspect
from logging.handlers import RotatingFileHandler

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)

PATH = os.path.dirname(os.path.abspath(__file__))

log_formatter = logging.Formatter('%(asctime)s: %(name)s - %(levelname)s - %(message)s')

logFile = '{}/XIQ_PoE_log.log'.format(parent_dir)

my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=10, encoding=None, delay=0)

my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

logger = logging.getLogger('root')
logger.setLevel(logging.INFO)

logger.addHandler(my_handler)

''' #TODO Remove section
logging.basicConfig(
	filename='{}/staggered_reboot.log'.format(parent_dir),
	filemode='a',
	level=os.environ.get("LOGLEVEL", "INFO"),
	format= '{}: %(name)s - %(levelname)s - %(message)s'.format(time.strftime("%Y-%m-%d %H:%M"))
)

logger = logging.getLogger("StaggeredReboot")

'''