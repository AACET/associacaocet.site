from pyding import on, EventCall
from stackhttp import Request, Response, HTTP
import logging

logger = logging.getLogger(__name__)

@on("http_request", host="links.associacaocet.site")
def links(event: EventCall, host, path, request, response: Response, server):
    response.define_code(201, "No Content")
    event.stop()
