from genericpath import isfile
import os
import re
from pyding import on, EventCall
from stackhttp import Request, Response, HTTP
import logging

logger = logging.getLogger(__name__)

@on("http_request", host="links.associacaocet.site")
def links(event: EventCall, host, path, request, response: Response, server):
    filename = os.path.basename(path)

    path = re.sub("[.]{2}|[~%]", "", path)
    path = os.path.join("assets/links/", path)

    while os.path.exists(path):
        if os.path.isdir(path):
            path = os.path.join(path, "index.html")
            
        elif os.path.isfile(path):
            response.send_file(path)         
            return event.stop()

    response.not_found()
    return event.stop()

