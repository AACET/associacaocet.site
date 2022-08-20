import logging
import ssl
from .structures import MailHandler, ControllerStarttls
from smtplib import SMTP as Client

global CONTROLLER
CONTROLLER = None
logger = logging.getLogger(__name__)


def start_mail_server():
    logger.info("Starting SMTPS server.")
    controller = ControllerStarttls(MailHandler('smtp.gmail.com', 587), "0.0.0.0", 25, server_hostname='Associacao Atletica de Ciencias Exatas e Tecnologias')
    controller.start()
    
    logger.info(f"SMTPS server is now running @ {controller.hostname} {controller.port}.")

def send_email(sender, recipient: list[str], message):
    logger.info(f"[SMTPS] Sending email to {recipient} from {sender}.")
    client = Client("associacaocet.site", 25)
    client.starttls(context=ssl.create_default_context())
    r = client.sendmail(sender, recipient, message)
    return r