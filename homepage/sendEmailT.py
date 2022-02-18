

import json
import threading
from django.core.mail import EmailMultiAlternatives



class SendEmailKanzi(threading.Thread):
    def __init__(self,subject,from_email,to_email,context,html,plain_text):
        self.subject =  subject
        self.from_email =  from_email
        self.to_email =  to_email
        self.context =  context
        self.html =  html
        self.plain_text =  plain_text
        threading.Thread.__init__(self)

    def run(self):
        subject, from_email, to = self.subject, self.from_email, self.to_email
        text_content = self.plain_text
        html_content = self.html.render(json.loads(json.dumps(self.context)))
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

