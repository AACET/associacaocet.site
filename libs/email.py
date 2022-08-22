from bs4 import BeautifulSoup
import logging
import dkim
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .structures import MailHandler, ControllerStarttls
 

global CONTROLLER
CONTROLLER = None
logger = logging.getLogger(__name__)


def start_mail_server():
    logger.info("Starting SMTPS server.")
    controller = ControllerStarttls(MailHandler(), "0.0.0.0", 25, server_hostname='Associacao Atletica de Ciencias Exatas e Tecnologias')
    controller.start()
    
    logger.info(f"SMTPS server is now running @ {controller.hostname} {controller.port}.")

def send_email(to_email, sender_email, subject, message_html, relay="clgw.correio.biz", dkim_private_key_path="/etc/dkim/private.pem", dkim_selector="mail"):
    # the `email` library assumes it is working with string objects.
    # the `dkim` library assumes it is working with byte objects.
    # this function performs the acrobatics to make them both happy.
    message_text = BeautifulSoup(message_html, 'html.parser').text
    sender_domain = sender_email.split("@")[-1]
    msg = MIMEMultipart("alternative")
    msg.attach(MIMEText(message_text, "plain"))
    msg.attach(MIMEText(message_html, "html"))
    msg["To"] = to_email
    msg["From"] = sender_email
    msg["Subject"] = subject
    try:
        # Python 3 libraries expect bytes.
        msg_data = msg.as_bytes()
    except:
        # Python 2 libraries expect strings.
        msg_data = msg.as_string()
    if dkim_private_key_path and dkim_selector:
        # the dkim library uses regex on byte strings so everything
        # needs to be encoded from strings to bytes.
        with open(dkim_private_key_path) as fh:
            dkim_private_key = fh.read()
        headers = [b"To", b"From", b"Subject"]
        sig = dkim.sign(
            message=msg_data,
            selector=str(dkim_selector).encode(),
            domain=sender_domain.encode(),
            privkey=dkim_private_key.encode(),
            include_headers=headers,
        )
        # add the dkim signature to the email message headers.
        # decode the signature back to string_type because later on
        # the call to msg.as_string() performs it's own bytes encoding...
        msg["DKIM-Signature"] = sig[len("DKIM-Signature: ") :].decode()
        try:
            # Python 3 libraries expect bytes.
            msg_data = msg.as_bytes()
        except:
            # Python 2 libraries expect strings.
            msg_data = msg.as_string()
    # TODO: react if connecting to relay (localhost postfix) is a socket error.
    s = smtplib.SMTP(relay)
    s.set_debuglevel(1)
    s.sendmail(sender_email, [to_email], msg_data)
    s.quit()
    return msg