import os
import re
import json
import httpx
import datetime

## Flask Imports
import flask
from flask import session
from flask import abort
from flask import url_for
from flask import redirect
from flask import current_app as app
from flask import send_from_directory
from flask import request
from flask_login import login_required, current_user

from app.routes import handler
from app.routes.bot import bot
from app.routes.auth import auth
from app.routes.logs import logsbot
from app.routes.execution import exe
from app.routes.dashboard import dash
from app.routes.credentials import cred
from app.routes.config import admin, supersu, usr
from app.models import Users
## Register Blueprints

listBlueprints = [
    bot, auth, logsbot,
    exe, dash, cred,
    admin, supersu, usr]

with app.app_context():
    
    for bp in listBlueprints:
        app.register_blueprint(bp)


@app.context_processor
def inject_user_cookies():
    
    admin_cookie, supersu_cookie = None, None
    
    if current_user.is_authenticated:
        admin_cookie = request.cookies.get('roles_admin')
        if admin_cookie:
            if json.loads(admin_cookie).get("login_id") != session["_id"]:
                admin_cookie = None
        
            supersu_cookie = request.cookies.get('roles_supersu')
            if supersu_cookie:
                if json.loads(supersu_cookie).get("login_id") != session["_id"]:
                    supersu_cookie = None
        
    return dict(admin_cookie=admin_cookie, supersu_cookie=supersu_cookie, current_user=current_user)


@app.route("/", methods=["GET"])
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
        abort(500, description=f"Erro interno do servidor: {str(e)}")


@app.route('/img/<user>.png', methods=["GET"])
@login_required
def serve_profile(user: str):

    try:
        with app.app_context():

            user = Users.query.filter(Users.login == user).first()
            image_data = user.blob_doc
            filename = user.filename
            
            if not image_data:
                
                url_image = "https://cdn-icons-png.freepik.com/512/13924/13924070.png"
                reponse_img = httpx.get(url_image)
                
                filename = os.path.basename(url_image)
                image_data = reponse_img.content
            
            
            image_data = bytes(image_data)
            filename = "".join(
                re.sub(r'[<>:"/\\|?*]', '_',
                       f"{datetime.datetime.now()}_{filename}"))
            
            original_path = os.path.join(
                app.config['IMAGE_TEMP_PATH'], filename)

            with open(original_path, 'wb') as file:
                file.write(image_data)

            response = flask.make_response(
                send_from_directory(app.config['IMAGE_TEMP_PATH'], filename))
            response.headers['Content-Type'] = 'image/png'
            
            return response

    except Exception as e:
        abort(500, description=f"Erro interno do servidor: {str(e)}")
