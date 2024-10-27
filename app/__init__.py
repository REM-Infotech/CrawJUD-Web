## Flask imports
from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

## Python Imports
import os
from dotenv import dotenv_values
from datetime import timedelta


## APP Imports
from configs import csp
from app import default_config

db = SQLAlchemy()
tlsm = Talisman()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "Faça login para acessar essa página."
login_manager.login_message_category = "info"


def create_app() -> tuple[Flask, int, bool]:

    src_path = os.path.join(os.getcwd(), "static")
    app = Flask(__name__, static_folder=src_path)

    app.config.from_object(default_config)
    age = timedelta(days=31).max.seconds
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app.models import init_database
        import app.routes
        
        
        
        init_database()
        tlsm.init_app(app, content_security_policy=csp(),
                      session_cookie_http_only=True,
                      session_cookie_samesite='Lax',
                      strict_transport_security_max_age=age,
                      x_content_type_options=True,
                      x_xss_protection=True)
    
    values = dotenv_values()
    
    ## Cloudflare Tunnel Configs
    port = int(values.get("PORT", 5000))
    debug = values.get('DEBUG', 'False').lower() in (
        'true', '1', 't', 'y', 'yes')
    
    
    return (app, port, debug)
