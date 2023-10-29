from . import forms
from datetime import datetime
import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    session,
)
from werkzeug.security import check_password_hash, generate_password_hash
from ...services.db import mongo
from .helper import (
    verify_password_reset_token,
    send_password_reset_email
)


bp = Blueprint("auth", __name__)

@bp.before_app_request
def load_logged_in_user():
    username = session.get("username")
    if username is None:
        g.user = None
    else:
        g.user = mongo.db.users.find_one({"username": username})
        print(g.user)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect("/login?next=" + request.path)
        return view(**kwargs)
    return wrapped_view



@bp.route("/reset/password", methods=["get", "post"])
def password_reset_request():
    if g.user:
        return redirect(url_for("portfolio.home"))
    form = forms.ResetPasswordRequestForm()
    if form.validate_on_submit():
        send_password_reset_email(form.email.data)
        flash("password reset link has been sent to " + form.email.data,
              "success")
        return redirect(url_for("auth.login"))
    return render_template(
        "auth/password-reset-request.html", title="reset password", form=form
    )

@bp.route("/reset/password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if g.user:
        return redirect(url_for("dashboard.home"))
    
    user = verify_password_reset_token(token)
    if user is None:
        flash(
            "That is an invalid or expired token! You can generate password reset link again.",
            "danger")
        return redirect(url_for("auth.password_reset_request"))
    
    tokens = mongo.db.users_reset_tokens
    reset_token = tokens.find_one({"token": token})
    if reset_token["password_changed"] == "Yes":
        flash(f"You already have changed password using this link.", "warning")
        return redirect(url_for("auth.login"))
    
    form = forms.ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user["password"] = hashed_password
        mongo.db.users.replace_one({'_id': user['_id']}, user)
        reset_token = tokens.find_one({"token": token})
        reset_token["password_changed"] = "Yes"
        tokens.replace_one({'_id': reset_token['_id']}, reset_token)
        flash("Your password has been updated!", "success")
        return redirect(url_for("auth.login"))
    
    return render_template(
        "auth/reset-password.html", title="Reset Password", form=form
    )


@bp.route("/register", methods=["GET", "POST"])
def register():
    if g.user is None:
        form = forms.SignupForm()
        if form.validate_on_submit():
            mongo.db.users.insert_one(
                {
                    "email": form.email.data,
                    "username": form.username.data,
                    "password": generate_password_hash(form.password.data),
                    "timestamp": datetime.now(),
                }
            )
            flash(f"Account created for {form.email.data}!", "success")
            return redirect(url_for("auth.login"))
        return render_template("auth/register.html",
                               form=form, title="Register")
    else:
        flash(f"Please logout first! ", "danger")
        return redirect(url_for("dashboard.home"))

@bp.route("/login", methods=["GET", "POST"])
@bp.route("/", methods=["GET", "POST"])
def login():
    if g.user:
        return redirect(url_for("dashboard.home"))
    form = forms.LoginForm()
    if form.validate_on_submit():
        users = mongo.db.users
        login_user = users.find_one({"username": form.username.data})
        if login_user and check_password_hash(
            login_user["password"], form.password.data
        ):
            session.clear()
            session["username"] = login_user["username"]
            flash("Logged in 😊️", "success")
            return (
                redirect(url_for("dashboard.home"))
            )
        else:
            flash("Incorrect username or password", "danger")
    return render_template("auth/login.html", form=form, title="Login")

@bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out 😊️", "success")
    return redirect(url_for("auth.login"))

@bp.route("/change/password", methods=["GET", "POST"])
@login_required
def change_password():
    form = forms.ChangePasswordForm()
    if form.validate_on_submit():
        if check_password_hash(g.user["password"], form.password.data):
            users = mongo.db.users
            user = users.find_one({"username": g.user["username"]})
            user["password"] = generate_password_hash(form.new_password.data)
            mongo.db.users.replace_one({'_id': user['_id']}, user )
            flash(f"Password has been changed succefully!", "success")
            return redirect(url_for("dashboard.home"))
        else:
            flash(f"Enter correct password!", "danger")
    return render_template(
        "auth/change-password.html", form=form, title="Change password"
    )

