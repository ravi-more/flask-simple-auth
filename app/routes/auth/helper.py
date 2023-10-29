from itsdangerous import URLSafeTimedSerializer as Serializer
from datetime import datetime
from ...services.db import mongo
from ...services.email import send_email

from flask import (
    url_for,
    current_app,
)


def verify_password_reset_token(token, expire_sec=1800):
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        email = s.loads(
            token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=expire_sec)["email"]
    except:
        return None
    return mongo.db.users.find_one({"email": email})


def generate_reset_token(email):
    s = Serializer(current_app.config["SECRET_KEY"])
    token = s.dumps({"email": email},
                    salt=current_app.config["SECURITY_PASSWORD_SALT"])
    tokens = mongo.db.users_reset_tokens
    tokens.update_many({"email": email}, {"$set": {"password_changed": "Yes"}})
    tokens.insert_one(
        {
            "email": email,
            "token": token,
            "time_generated": datetime.now(),
            "password_changed": "No",
        }
    )
    return token


def send_password_reset_email(email):
    token = generate_reset_token(email, )
    subject = "Flask Simple Auth Password Reset"
    text_body = f"""To reset your password, view link:
    {url_for('auth.reset_password', token=token, _external=True)}
    """
    send_email(
        sender="Flask Simple Auth",
        recipients=[email],
        subject=subject,
        text_body=text_body,
    )
