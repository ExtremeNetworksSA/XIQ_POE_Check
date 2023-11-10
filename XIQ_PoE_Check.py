#!/usr/bin/env python3
import logging
import os
import inspect
from app.logger import logger
from app.xiq_api import XIQ
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
logger = logging.getLogger('StaggeredReboot.Main')

XIQ_API_token = ''

pageSize = 100