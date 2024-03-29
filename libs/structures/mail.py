from aiosmtpd.smtp import SMTP
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Proxy
import ssl
import smtplib
from .. import config
import logging

log = logging.getLogger(__name__)

class MailHandler:
    async def handle_DATA(self, server, session, envelope):
        print('Message from %s' % envelope.mail_from)
        print('Message for %s' % envelope.rcpt_tos)
        print('Message data:\n')
        for ln in envelope.content.decode('utf8', errors='replace').splitlines():
            print(f'> {ln}'.strip())
        print()
        print('End of message')
        return '205 OK'

class ControllerStarttls(Controller):
    def factory(self):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(config.get_chain_path(), config.get_private_key_path())
        return SMTP(self.handler, require_starttls=True, tls_context=context)
