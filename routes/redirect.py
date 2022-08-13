from pyding import on, EventCall
from stackhttp import Request, Response, HTTP
import logging

logger = logging.getLogger(__name__)

@on("http_request", priority=float("-inf"))
def links(event: EventCall, host, path, request, response: Response, server):
    response.define_code(301, "Permanently Moved")
    response.headers["Location"] = "https://links.associacaocet.site/"
    event.stop()
