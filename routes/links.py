
from genericpath import isfile
import os
import re
from pyding import on, EventCall
from stackhttp import Request, Response, HTTP
import logging

from libs.utils import fetch_files

logger = logging.getLogger(__name__)

@on("http_request", host="links.associacaocet.site")
def links(event: EventCall, host, path, request, response: Response, server):
    fetch_files('links', path, response)
    return event.stop()

