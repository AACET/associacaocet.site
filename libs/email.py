import logging
from .structures import MailHandler
from aiosmtpd.controller import Controller, ControllerStarttls
from smtplib import SMTP as Client

CONTROLLER = None
logger = logging.getLogger(__name__)


def start_mail_server():
    logger.info("Starting SMTPS server.")
    CONTROLLER = ControllerStarttls(MailHandler, "0.0.0.0", 587)
    CONTROLLER.start()
    logger.info("SMTPS server is now running.")

def send_email(sender, recipient: list[str], message):
    logger.info(f"[SMTPS] Sending email to {recipient} from {sender}.")
    client = Client(CONTROLLER.hostname, CONTROLLER.port)
    r = client.sendmail(sender, recipient, message)
    return r