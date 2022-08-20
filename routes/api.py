from genericpath import isfile
from libs import email
from pyding import on, EventCall
from stackhttp import Request, Response, HTTP
import logging

logger = logging.getLogger(__name__)

@on("http_request", host="api.associacaocet.site")
def links(event: EventCall, host, path, request: Request, response: Response, server):
    response.forbidden()
    match request.method, path.removeprefix("/").split("/"):
        case 'POST', ["mail", "test"]:
            logger.info("Sending email")
            email.send_email('do_not_reply@associacaocet.site', 'bernarditete6@gmail.com', 'Hello world from API')
            response.ok(json={'sent': True})
    
    return event.stop()

