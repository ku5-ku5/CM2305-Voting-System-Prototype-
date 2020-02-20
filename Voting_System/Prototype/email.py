from Prototype import mail, app
from flask_mail import Message
from flask import render_template

def send_mail(to,subject,template):
    msg = Message(subject=subject,sender='vote.prototype@gmail.com', recipients=to)
    msg.html=render_template(template)
    mail.send(msg)