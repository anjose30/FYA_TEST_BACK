# credit/utils/email_utils.py
import threading
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        try:
            send_mail(
                self.subject,
                self.message,
                settings.EMAIL_HOST_USER,
                self.recipient_list,
                fail_silently=False,
            )
            logger.info(f"Correo enviado exitosamente a {self.recipient_list}")
        except Exception as e:
            logger.error(f"Error enviando correo: {str(e)}")

def send_async_email(subject, message, recipient_list):
    EmailThread(subject, message, recipient_list).start()