from flask import Flask
import os
from .services.db import mongo
from flask_mail import Mail
mail = Mail()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py", silent=True)
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass
    mongo.init_app(app)
    mail.init_app(app)
    from .routes import auth
    app.register_blueprint(auth.bp)
    from .routes import dashboard
    app.register_blueprint(dashboard.bp)

    return app
