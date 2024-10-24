import os

## Flask Imports
from flask import abort
from flask import url_for
from flask import redirect
from flask import current_app as app
from flask import send_from_directory


from app.routes import handler
from app.routes.bot import bot
from app.routes.auth import auth
from app.routes.logs import logsbot
from app.routes.execution import exe
from app.routes.dashboard import dash
from app.routes.credentials import cred
from app.routes.config import admin, supersu, usr

## Register Blueprints

listBlueprints = [
    bot, auth, logsbot, 
    exe, dash, cred, 
    admin, supersu, usr
    ]

with app.app_context():
    
    for bp in listBlueprints:
        app.register_blueprint(bp)
    

@app.route("/", methods = ["GET"])
def index():
    
    return redirect(url_for("auth.login")), 302


@app.route('/favicon.png', methods=["GET"])
def serve_img():

    try:
        
        paht_icon = os.path.join(os.getcwd(), "static", "img")
        url = send_from_directory(paht_icon, "crawjud.png")
        return url

    except Exception as e:
        print(e)
        abort(500)