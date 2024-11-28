# Flask imports
# Python Imports
import os
from datetime import timedelta
from importlib import import_module
from pathlib import Path

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

from app import default_config
# APP Imports
from configs import csp

db = SQLAlchemy()
tlsm = Talisman()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Faça login para acessar essa página."
login_manager.login_message_category = "info"


class AppFactory:

    def init_extensions(self, app: Flask):

        db.init_app(app)
        mail.init_app(app)
        login_manager.init_app(app)

        with app.app_context():

            self.init_database(app, db)

            tlsm.init_app(
                app,
                content_security_policy=csp(),
                force_https_permanent=True,
                force_https=True,
                session_cookie_http_only=True,
                session_cookie_samesite="Lax",
                strict_transport_security_max_age=timedelta(days=31).max.seconds,
                x_content_type_options=True,
                x_xss_protection=True,
            )
            import_module("app.routes", __package__)

    def create_app(self) -> Flask:
        """
        Construtor do app Flask

        """
        src_path = os.path.join(os.getcwd(), "static")
        app = Flask(__name__, static_folder=src_path)

        app.config.from_object(default_config)
        self.init_extensions(app)
        self.init_blueprints(app)

        """ Initialize logs module """

        from app.logs.setup import initialize_logging

        app.logger = initialize_logging()

        return app

    def init_blueprints(self, app: Flask):
        """
        Registro de blueprints

        :param Flask app: Aplicativo Flask

        """
        from app.routes.auth import auth
        from app.routes.bot import bot
        from app.routes.config import admin, supersu, usr
        from app.routes.credentials import cred
        from app.routes.dashboard import dash
        from app.routes.execution import exe
        from app.routes.logs import logsbot

        listBlueprints = [bot, auth, logsbot, exe, dash, cred, admin, supersu, usr]

        for bp in listBlueprints:
            app.register_blueprint(bp)

    def init_database(self, app: Flask, db: SQLAlchemy):

        from app.models import init_database

        if not Path("is_init.txt").exists():

            with open("is_init.txt", "w") as f:
                f.write(f"{init_database(app, db)}")


create_app = AppFactory().create_app
