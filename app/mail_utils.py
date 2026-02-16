from .extensions import mail
from flask_mail import Message
from flask import render_template

def send_reset_email(to_email, reset_link):
    msg = Message(
        "Business Dashboard",
        recipients=[to_email],
        html= render_template("auth/reset_email.html", reset_link=reset_link),
        body= render_template("auth/reset_email.txt", reset_link=reset_link)
    )
    mail.send(msg)