from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from app import default_config
from configs import csp

import os
import json
import pathlib
from dotenv import dotenv_values
from datetime import timedelta
from cloudflare import run_with_cloudflared

db = SQLAlchemy()
tlsm = Talisman()
mail = Mail()
login_manager = LoginManager()

def create_app():

    src_path = os.path.join(os.getcwd(), "static")
    app = Flask(__name__, static_folder=src_path)

    app.config.from_object(default_config)
    

    from app.models import init_database
    age = timedelta(days=31).max.seconds
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    tlsm.init_app(app, content_security_policy=csp(),
                session_cookie_http_only=True,
                session_cookie_samesite='Lax',
                strict_transport_security=True,
                strict_transport_security_max_age=age,
                x_content_type_options= True,
                x_xss_protection=True)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Faça login para acessar essa página."
    login_manager.login_message_category = "info"
    init_database(app)
    
    
    path_main = pathlib.Path(__file__).parent.resolve()
    values = dotenv_values()
    debug = values.get("DEBUG", "False").lower() in ("true", "1", "t", "y", "yes")
    
    ## Cloudflare Tunnel Configs
    hostname = values.get("HOSTNAME")
    port = values.get("PORT", 5000)
    tunnel = values.get("TUNNEL_ID")
    credentials = json.loads(values.get("CREDENTIALS_TUNNEL"))

    ## Set credentials and config.yml path
    credentials_json = os.path.join(path_main, "credentials.json")
    config_yml = os.path.join(path_main, "config.yml")
    
    
    ## Config Content
    config_content = f"""
tunnel: {tunnel}
credentials-file: {credentials_json}

ingress:
    - hostname: {hostname}
      service: http://127.0.0.1:{port}
    - service: http_status:404
    """

    
    ## Save the configuration and credentials content into files
    with open(config_yml, 'w') as file:
        content = file.write(config_content)
        
    with open(credentials_json, "w") as f:
        f.write(json.dumps(credentials))
    
    
    from app.routes import  blueprint_reg
    
    blueprint_reg(app)
    
    return app


