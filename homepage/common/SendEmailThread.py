from django.core.mail import EmailMessage
import threading

class SendEmailThread(threading.Thread):
    def __init__(self,email,message,subject):
        self.email = email
        self.message = message
        self.subject = subject
        threading.Thread.__init__(self)

    def run(self):
        
        to_email = self.email
        email = EmailMessage(self.subject, self.message, to=[to_email])
        email.send()
