import logging
from pyding import on, EventCall
from stackhttp import Request, Response, HTTP
import os
import logging

logger = logging.getLogger(__name__)

@on("http_request", priority=100)
def links(event: EventCall, host, path, request: Request, response: Response, server):
    if not path:
        response.internal_server_error()
        event.stop()

    match os.path.basename(path):
        case "favicon.ico" as name:
            logging.info(f"Serving {name}")
            response.not_found()
            event.stop()

