import os
import logging
import traceback
import sys

logger = logging.getLogger(__name__)

def load_routes():
    for handler in os.listdir("routes"):
        if handler.endswith(".py"):
            try:
                __import__("routes."+handler.removesuffix(".py"))
                logging.getLogger('routes.'+handler.removesuffix(".py")).addHandler(
                    logging.FileHandler(
                        'logs/routes.'+handler.removesuffix(".py")+".log"
                    )
                )
                logger.info(f'Loaded {handler}')
            except:
                logger.error(f"Failed to load handler {handler}")
                traceback.print_exc(file=sys.stdout)
