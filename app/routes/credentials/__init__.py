from app.models import Credentials, BotsCrawJUD
from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required
import os
import pathlib

from collections import Counter

from app.forms.credentials import CredentialsForm


path_template = os.path.join(pathlib.Path(
    __file__).parent.resolve(), "templates")
cred = Blueprint("creds", __name__, template_folder=path_template)


@cred.route("/credentials/dashboard", methods=["GET"])
def credentials():

    title = "Credenciais"
    page = "credentials.html"
    return render_template("index.html", page=page, title=title)

@cred.route("/credentials/cadastro", methods=["GET", "POST"])
@login_required
def cadastro():

    page = "FormCred.html"
    
    systems = [bot.system for bot in BotsCrawJUD.query.all()]
    count_system = Counter(systems).keys()
    
    system = [system for system in count_system]
    
    form = CredentialsForm(**{
        "system": system
    })

    func = "Cadastro"
    title = "Credenciais"

    
    
    
    
    
    
    action_url = url_for('creds.cadastro')

    if form.validate_on_submit():
        return redirect(url_for("creds.credentials"))

    return render_template("index.html", page=page, form=form,
                           title=title, func=func, action_url=action_url)

