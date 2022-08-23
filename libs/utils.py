import os
import logging
import traceback
import sys
import re

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

def fetch_files(assets_code, path, response):
    filename = os.path.basename(path)

    path = re.sub("[.]{2}|[~%]", "", path.removeprefix("/"))
    path = os.path.join("assets", assets_code, path)

    while os.path.exists(path):
        if os.path.isdir(path):
            path = os.path.join(path, "index.html")
            
        elif os.path.isfile(path):
            logger.info(f"Serving [{path}]")
            response.send_file(path)         

    response.not_found()