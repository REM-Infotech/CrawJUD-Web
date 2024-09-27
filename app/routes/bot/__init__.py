from app.models import BotsCrawJUD, LicensesUsers
from flask import (Blueprint, render_template,
                   request, url_for, redirect, session)
from flask_login import login_required
import os
import pathlib

from app.forms import BotForm

path_template = os.path.join(pathlib.Path(
    __file__).parent.resolve(), "templates")
bot = Blueprint("bot", __name__, template_folder=path_template)

FORM_CONFIGURATOR = {
    
    "JURIDICO":{
        "file_auth": ["xlsx", "creds", "state"],
        "multipe_files": ["xlsx", "creds", "state", "otherfiles"],
        "only_file": ["xlsx", "state"],
    },
    "ADMINISTRATIVO":{
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

    page = "botboard.html"
    bots = BotsCrawJUD.query.all()

    return render_template("index.html", page=page, bots=bots)


@bot.route("/bot/<id>/<system>/<type>", methods=["GET", "POST"])
@login_required
def botlaunch(id: int, system: str, type: str):

    bot_info = BotsCrawJUD.query.filter_by(id=id).first()
    display_name = bot_info.display_name
    
    states = [(state.state, state.state) for state in BotsCrawJUD.query.filter(
        BotsCrawJUD.type == type.upper(), BotsCrawJUD.system == system.upper()).all()]

    creds = LicensesUsers.query.filter(
        LicensesUsers.license_token == session["license_token"]).first()
    
    credts: list[tuple[str, str]] = []
    for credential in creds.credentials:
        if credential.system == system.upper():
            credts.append((credential.nome_credencial, credential.nome_credencial))

    
    page = "botform.html"
    form = BotForm(dynamic_fields=FORM_CONFIGURATOR[
        bot_info.classification][bot_info.form_cfg], **{
        "state": states,
        "creds": credts
    })
    
    if form.validate_on_submit():
        return redirect(url_for("dash.dashboard"))
        
    return render_template("index.html", page=page, url=request.base_url,
                           display_name=display_name, form=form)
