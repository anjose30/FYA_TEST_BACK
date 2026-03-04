import threading
import resend
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        try:
            print(">>> Iniciando envío de correo")
            resend.api_key = settings.RESEND_API_KEY
            print(f">>> API KEY: {settings.RESEND_API_KEY}")
            print(f">>> FROM: {settings.EMAIL_FROM}")
            print(f">>> TO: {self.recipient_list}")

            params = {
                "from": settings.EMAIL_FROM,
                "to": self.recipient_list,
                "subject": self.subject,
                "text": self.message,
            }

            response = resend.Emails.send(params)
            print(f">>> Respuesta Resend: {response}")
            logger.info(f"Correo enviado exitosamente a {self.recipient_list}")
        except Exception as e:
            print(f">>> ERROR: {str(e)}")
            logger.error(f"Error enviando correo: {str(e)}", exc_info=True)

def send_async_email(subject, message, recipient_list):
    EmailThread(subject, message, recipient_list).start()