from flask import current_app
from flask_mail import Message
from app import mail


def send_email(sender, subject, recipients, text_body=None, html_body=None):
    msg = Message(
        subject=subject,
        sender=(sender, current_app.config["MAIL_USERNAME"]),
        recipients=recipients,
        body=text_body,
        html=html_body,
    )
    mail.send(msg)
