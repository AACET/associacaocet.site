import logging
from structures import MailHandler
from aiosmtpd.controller import Controller
from smtplib import SMTP as Client
import ssl
from . import config

CONTROLLER = None
logger = logging.getLogger(__name__)

def start_mail_server():
    logger.info("Loading ssl context.")
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(config.get_chain_path(), config.get_private_key_path())
    logger.info("Starting SMTPS server.")
    CONTROLLER = Controller(MailHandler, "0.0.0.0", 587, ssl_context=context)
    CONTROLLER.start()
    logger.info("SMTPS server is now running.")

def send_email(sender, recipient: list[str], message):
    logger.info(f"[SMTPS] Sending email to {recipient} from {sender}.")
    client = Client(CONTROLLER.hostname, CONTROLLER.port)
    r = client.sendmail(sender, recipient, message)
    return r