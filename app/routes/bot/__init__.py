from flask import (Blueprint, render_template, request, flash,
                   url_for, redirect, session, current_app, jsonify)
from flask_login import login_required
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

import os
import json
import pathlib
import httpx
from typing import Union
from datetime import datetime
from datetime import date
from contextlib import suppress

from app import db
from app.forms import BotForm
from app.misc import generate_pid
from app.models import BotsCrawJUD, LicensesUsers, Servers, Credentials
from requests.exceptions import ConnectTimeout

path_template = os.path.join(pathlib.Path(
    __file__).parent.resolve(), "templates")
bot = Blueprint("bot", __name__, template_folder=path_template)

FORM_CONFIGURATOR = {

    "JURIDICO": {
        "file_auth": ["xlsx", "creds", "state"],
        "multipe_files": ["xlsx", "creds", "state", "otherfiles"],
        "only_file": ["xlsx", "state"],
        "pautas": ["data_inicio", "data_fim", "creds", "state", "varas"],
        "proc_parte": ["parte_name", "doc_parte", "data_inicio", "data_fim", 
                       "polo_parte", "state", "varas", "creds"]
    },
    "ADMINISTRATIVO": {
        "file_auth": ["xlsx", "creds", "client"],
        "multipe_files": ["xlsx", "creds", "client", "otherfiles"]

    },
    "INTERNO": {
        "multipe_files": ["xlsx", "otherfiles"]
    }

}


@bot.route("/bot/dashboard", methods=["GET"])
@login_required
def dashboard():

    title = "Robôs"
    page = "botboard.html"
    bots = BotsCrawJUD.query.all()

    return render_template("index.html", page=page, bots=bots, title=title)


@bot.route("/bot/<id>/<system>/<typebot>", methods=["GET", "POST"])
@login_required
def botlaunch(id: int, system: str, typebot: str):

    bot_info = BotsCrawJUD.query.filter_by(id=id).first()
    display_name = bot_info.display_name
    title = display_name

    states = [(state.state, state.state) for state in BotsCrawJUD.query.filter(
        BotsCrawJUD.type == typebot.
        upper(), BotsCrawJUD.system == system.upper()).all()]

    clients = [(client.client, client.client) for client in BotsCrawJUD.query.filter(
        BotsCrawJUD.type == typebot.
        upper(), BotsCrawJUD.system == system.upper()).all()]

    creds = db.session.query(Credentials).\
        join(LicensesUsers).\
        filter(LicensesUsers.license_token == session["license_token"]).\
        all()

    credts: list[tuple[str, str]] = []
    for credential in creds:
        if credential.system == system.upper():
            credts.append((credential.nome_credencial,
                          credential.nome_credencial))

    form_config = []

    classbot = str(bot_info.classification)
    form_setup = str(bot_info.form_cfg)

    if typebot.\
            upper() == "PAUTA" and system.upper() == "PJE":
        form_setup = "pautas"
        
    elif typebot.lower() == "proc_parte":
        form_setup = "proc_parte"
    
    form_config.extend(FORM_CONFIGURATOR[classbot][form_setup])

    if system.upper() == "PROJUDI" and typebot.\
            upper() == "PROTOCOLO" and bot_info.state == "AM":
        form_config.append("password")

    page = "botform.html"
    form = BotForm(dynamic_fields=form_config, **{
        "state": states,
        "creds": credts,
        "clients": clients,
        "system": system
    })
    temporarypath = current_app.config["TEMP_PATH"]
    if form.validate_on_submit():

        data = {}
        pid = generate_pid()
        data.update({
            "pid": pid,
            "user": session["login"]
        })

        headers = {'CONTENT_TYPE': request.environ['CONTENT_TYPE']}
        data_form: dict[
            str, Union[
                str, datetime,
                FileStorage, list[FileStorage],
                list[str]]] = form.data.items()

        files = {}
        for item, value in data_form:
            if isinstance(value, FileStorage):

                data.update({"xlsx": secure_filename(value.filename)})
                value.save(os.path.join(temporarypath,
                           secure_filename(value.filename)))
                buff = open(os.path.join(temporarypath,
                            secure_filename(value.filename)), "rb")
                
                buff.seek(0)
                files.update({secure_filename(value.filename): (
                    secure_filename(value.filename), buff, value.mimetype)})

            if isinstance(value, list):

                if not isinstance(value[0], FileStorage):
                    data.update({item: value})
                    continue

                for filev in value:
                    if isinstance(filev, FileStorage):
                        filev.save(os.path.join(temporarypath,
                                                secure_filename(filev.filename)))
                        buff = open(os.path.join(temporarypath,
                                    secure_filename(filev.filename)), "rb")
                        files.update({secure_filename(filev.filename): (
                            secure_filename(filev.filename), buff, filev.mimetype)})

            if not isinstance(value, FileStorage):

                if item == "creds":
                    for credential in creds:
                        if credential.nome_credencial == value:
                            if credential.login_method == "pw":
                                data.update({
                                    "username": credential.login,
                                    "password": credential.password,
                                    "login_method": credential.login_method
                                })

                            if credential.login_method == "cert":
                                certpath = os.path.join(
                                    temporarypath, credential.certficate)
                                with open(certpath, "wb") as f:
                                    f.write(credential.certficate_blob)

                                buff = open(os.path.join(certpath), "rb")
                                files.update({credential.certficate: (
                                    credential.certficate, buff)})
                                data.update({
                                    "username": credential.login,
                                    "name_cert": credential.certficate,
                                    "token": credential.key,
                                    "login_method": credential.login_method
                                })
                            break

                data.update({item: value})
                if isinstance(value, date):
                    data.update({item: value.strftime("%Y-%m-%d")})

                if item == "password" and system.upper() == "PROJUDI" and typebot.\
                        upper() == "PROTOCOLO" and bot_info.state == "AM":

                    data.update({"token": value})

        servers = Servers.query.all()
        for server in servers:
            data.update({
                "url_socket": server.address
            })
            
            kwargs: dict[str, str] = {
                "url": f"https://{server.address}{request.path}", 
                "json":json.dumps(data)}
            
            if files:
                kwargs.pop("json")
                kwargs.update({"files": files, "data": data})
            response = None
            
            with suppress(httpx.ConnectTimeout):
                response = httpx.post(timeout=60, **kwargs)
                
            if response:    
                if response.status_code == 200:
                    message = f"Execução iniciada com sucesso! PID: {pid}"
                    flash(message, "success")
                    return redirect(url_for("logsbot.logs_bot", sid=pid))

                elif response.status_code == 500:
                    pass
            
        flash("Erro ao iniciar robô", "error")

    return render_template("index.html", page=page, url=request.base_url,
                           display_name=display_name, form=form, title=title)
