import datetime
import json
import os
import re

import httpx
from deep_translator import GoogleTranslator

# Flask Imports
from flask import abort
from flask import current_app as app
from flask import (
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask_login import current_user, login_required
from werkzeug.exceptions import HTTPException


@app.context_processor
def inject_user_cookies():

    admin_cookie, supersu_cookie = None, None

    if current_user.is_authenticated:
        admin_cookie = request.cookies.get("roles_admin")
        if admin_cookie:
            if json.loads(admin_cookie).get("login_id") != session["_id"]:
                admin_cookie = None

            supersu_cookie = request.cookies.get("roles_supersu")
            if supersu_cookie:
                if json.loads(supersu_cookie).get("login_id") != session["_id"]:
                    supersu_cookie = None

    return dict(
        admin_cookie=admin_cookie,
        supersu_cookie=supersu_cookie,
        current_user=current_user,
    )


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("auth.login")), 302


@app.route("/favicon.png", methods=["GET"])
def serve_img():

    try:

        paht_icon = os.path.join(os.getcwd(), "static", "img")
        url = send_from_directory(paht_icon, "crawjud.png")
        return url

    except Exception as e:
        print(e)
        abort(500, description=f"Erro interno do servidor: {str(e)}")


@app.route("/img/<user>.png", methods=["GET"])
@login_required
def serve_profile(user: str):

    try:
        with app.app_context():

            from app.models import Users

            user = Users.query.filter(Users.login == user).first()
            image_data = user.blob_doc
            filename = user.filename

            if not image_data:

                url_image = "https://cdn-icons-png.flaticon.com/512/3135/3135768.png"
                reponse_img = httpx.get(url_image)

                filename = os.path.basename(url_image)
                image_data = reponse_img.content

            image_data = bytes(image_data)
            filename = "".join(
                re.sub(r'[<>:"/\\|?*]', "_", f"{datetime.datetime.now()}_{filename}")
            )

            original_path = os.path.join(app.config["IMAGE_TEMP_PATH"], filename)

            with open(original_path, "wb") as file:
                file.write(image_data)

            response = make_response(
                send_from_directory(app.config["IMAGE_TEMP_PATH"], filename)
            )
            response.headers["Content-Type"] = "image/png"

            return response

    except Exception as e:
        abort(500, description=f"Erro interno do servidor: {str(e)}")


@app.errorhandler(HTTPException)
def handle_http_exception(error):

    tradutor = GoogleTranslator(source="en", target="pt")
    name = tradutor.translate(error.name)
    desc = tradutor.translate(error.description)

    return (
        render_template("handler/index.html", name=name, desc=desc, code=error.code),
        error.code,
    )
