from flask import (Blueprint, render_template, request, flash,
                   url_for, redirect, session, current_app)
from flask_login import login_required
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

import os
import pathlib
import requests

from app.forms import BotForm
from app.misc import generate_pid
from app.models import BotsCrawJUD, LicensesUsers, Servers


path_template = os.path.join(pathlib.Path(
    __file__).parent.resolve(), "templates")
bot = Blueprint("bot", __name__, template_folder=path_template)

FORM_CONFIGURATOR = {

    "JURIDICO": {
        "file_auth": ["xlsx", "creds", "state"],
        "multipe_files": ["xlsx", "creds", "state", "otherfiles"],
        "only_file": ["xlsx", "state"],
        "catchall": ["xlsx", "creds", "state", "varas"]
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


@bot.route("/bot/<id>/<system>/<type>", methods=["GET", "POST"])
@login_required
def botlaunch(id: int, system: str, type: str):

    
    bot_info = BotsCrawJUD.query.filter_by(id=id).first()
    display_name = bot_info.display_name
    title = display_name
    
    states = [(state.state, state.state) for state in BotsCrawJUD.query.filter(
        BotsCrawJUD.type == type.upper(), BotsCrawJUD.system == system.upper()).all()]

    clients = [(client.client, client.client) for client in BotsCrawJUD.query.filter(
        BotsCrawJUD.type == type.upper(), BotsCrawJUD.system == system.upper()).all()] 
    
    creds = LicensesUsers.query.filter(
        LicensesUsers.license_token == session["license_token"]).first()

    credts: list[tuple[str, str]] = []
    for credential in creds.credentials:
        if credential.system == system.upper():
            credts.append((credential.nome_credencial,
                          credential.nome_credencial))
            
    form_config = []
    
    classbot = str(bot_info.classification)
    form_setup = str(bot_info.form_cfg)
    
    if any(type.upper() == tipobot for tipobot in ["PAUTA", "PROC_PARTE"]):
        form_setup = "catchall"
        
    form_config.extend(FORM_CONFIGURATOR[classbot][form_setup])
    
    if system.upper() == "PROJUDI" and type.upper() == "PROTOCOLO" and bot_info.state == "AM":
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
        data_form = form.data.items()
        files = {}
        for item, value in data_form:
            if isinstance(value, FileStorage):

                data.update({"xlsx": secure_filename(value.filename)})
                value.save(os.path.join(temporarypath, secure_filename(value.filename)))
                buff = open(os.path.join(temporarypath,secure_filename(value.filename)), "rb")
                files.update({ secure_filename(value.filename): (secure_filename(value.filename), buff, value.mimetype)})
                
            if isinstance(value, list):
                
                for filev in value:
                    filev.save(os.path.join(temporarypath, secure_filename(filev.filename)))
                    buff = open(os.path.join(temporarypath,secure_filename(filev.filename)), "rb")
                    files.update({ secure_filename(filev.filename): (secure_filename(filev.filename), buff, filev.mimetype)})
                    
                
            if not isinstance(value, FileStorage):

                if item == "creds":
                    for credential in creds.credentials:
                        if credential.nome_credencial == value:
                            if credential.login_method == "pw":
                                data.update({
                                    "login": credential.login,
                                    "password": credential.password,
                                    "login_method": credential.login_method
                                })
                                
                                
                            if credential.login_method == "cert":
                                certpath = os.path.join(temporarypath, credential.certficate)
                                with open(certpath , "wb") as f:
                                    f.write(credential.certficate_blob)
                                
                                buff = open(os.path.join(certpath), "rb")
                                files.update({credential.certficate: (credential.certficate, buff)})
                                data.update({
                                    "login": credential.login,
                                    "name_cert": credential.certficate,
                                    "token": credential.key,
                                    "login_method": credential.login_method
                                })
                            break
                
                if item == "password" and system.upper() == "PROJUDI" and type.upper() == "PROTOCOLO" and bot_info.state == "AM":
                    data.update({"token": value})

                if item == "state":
                    data.update({"state": value})
                    
                elif item == "client":
                    data.update({"client": value})
                
        servers = Servers.query.all()
        for server in servers:
            data.update({
                "url_socket": server.address
            })
            response = requests.post(f"https://{server.address}{request.path}", data=data, headers=headers, files=files)
            if response.status_code == 200:
                flash(f"Execução iniciada dashcom sucesso! PID: {pid}", "success")
                return redirect(url_for("logsbot.logs_bot", sid=pid))

        flash("Erro ao iniciar robô", "error")
        
    return render_template("index.html", page=page, url=request.base_url,
                           display_name=display_name, form=form, title=title)
