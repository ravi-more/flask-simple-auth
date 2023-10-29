from ...services.db import mongo
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError
)
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
)


class SignupForm(FlaskForm):
    email = StringField(
        "Email*", validators=[DataRequired(), Length(min=3, max=100), Email()])
    username = StringField(
        "Username*", validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField("Password", validators=[DataRequired(
        message="Please provide password"), Length(
            min=8, message="Provide at least 8 characters")])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = mongo.db.users.find_one({"username": username.data})
        if user:
            raise ValidationError("Username already exist!")

    def validate_email(self, email):
        user = mongo.db.users.find_one({"email": email.data})
        if user:
            raise ValidationError("Username already exist!")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(
        message="Please provide password"), Length(
            min=8, message="Provide at least 8 characters")])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(
        "Email*", validators=[DataRequired(), Length(min=3, max=100), Email()])
    submit = SubmitField("Send link")

    def validate_email(self, email):
        user = mongo.db.users.find_one({"email": email.data})
        if user == None:
            raise ValidationError("Username not exist!")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(
        message="Please provide password"), Length(
            min=8, message="Provide at least 8 characters")])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    reset = SubmitField("Reset password")


class ChangePasswordForm(FlaskForm):
    password = PasswordField("Enter current password",
                             validators=[DataRequired()])
    new_password = PasswordField(
        "Enter new password", validators=[DataRequired(
            message="Please provide password"), Length(
            min=8, message="Provide at least 8 characters")])
    confirm_new_password = PasswordField(
        "Confirm new password", validators=[DataRequired(),
                                            EqualTo("new_password")]
    )
    submit = SubmitField("Change Password")
