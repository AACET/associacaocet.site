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
    client = Client('gmail-smtp-in.l.google.com', 25)
    client.set_debuglevel(1)
    client.ehlo('associacaocet.site')
    client.starttls()
    client.ehlo('associacaocet.site')
    client.mail(sender)
    client.rcpt(recipient)
    client.data(message)
    client.quit()
    return