from aiosmtpd.smtp import SMTP
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Proxy
import ssl
import smtplib
from .. import config
import logging

log = logging.getLogger(__name__)

class MailHandler(Proxy):
    async def handle_DATA(self, server, session, envelope):
        print('Message from %s' % envelope.mail_from)
        print('Message for %s' % envelope.rcpt_tos)
        print('Message data:\n')
        for ln in envelope.content.decode('utf8', errors='replace').splitlines():
            print(f'> {ln}'.strip())
        print()
        print('End of message')
        return await super().handle_DATA(server, session, envelope)
    
    def _deliver(self, mail_from, rcpt_tos, data):
        refused = {}
        try:
            s = smtplib.SMTP()
            s.connect(self._hostname, self._port)
            s.starttls()
            try:
                refused = s.sendmail(mail_from, rcpt_tos, data)
            finally:
                s.quit()
        except smtplib.SMTPRecipientsRefused as e:
            log.info('got SMTPRecipientsRefused')
            refused = e.recipients
        except (OSError, smtplib.SMTPException) as e:
            log.exception('got %s', e.__class__)
            # All recipients were refused.  If the exception had an associated
            # error code, use it.  Otherwise, fake it with a non-triggering
            # exception code.
            errcode = getattr(e, 'smtp_code', -1)
            errmsg = getattr(e, 'smtp_error', 'ignore')
            for r in rcpt_tos:
                refused[r] = (errcode, errmsg)
        return refused

class ControllerStarttls(Controller):
    def factory(self):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(config.get_chain_path(), config.get_private_key_path())
        return SMTP(self.handler, require_starttls=True, tls_context=context)
