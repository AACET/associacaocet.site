from genericpath import isfile
import os
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
            file = open(os.path.join('assets', 'emails', 'welcome.html'), 'r')
            email.send_email('bernarditete6@gmail.com', 'sistema@associacaocet.site', '[SISTEMA]: Email de teste de envio', file.read())
            file.close()
            response.ok(json={'sent': True})
    
    return event.stop()

