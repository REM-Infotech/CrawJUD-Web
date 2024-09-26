from app.models import Credentials, BotsCrawJUD, LicensesUsers
from flask import Blueprint, render_template, session, url_for, redirect, flash
from flask_login import login_required
from app import db

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
    
    system = [(syst, syst) for syst in count_system]
    
    form = CredentialsForm(**{
        "system": system
    })

    func = "Cadastro"
    title = "Credenciais"

    action_url = url_for('creds.cadastro')

    if form.validate_on_submit():
        
        if Credentials.query.filter(
            Credentials.nome_credencial == form.nome_cred.data).first():
            flash("Existem credenciais com este nome já cadastrada!", "error")
            return redirect(url_for("creds.cadastro"))
        

        def pw(form):
            
            passwd = Credentials(
                nome_credencial = form.nome_cred.data,
                system = form.system.data,
                login_method = form.auth_method.data,
                login = form.login.data,
                password = form.password.data
            )
            db.session.add(passwd)
            licenseusr = LicensesUsers.query.filter(
                LicensesUsers.license_token == session["license_token"]).first()
            licenseusr.credentials.append(passwd)
            db.session.commit()
            
        def cert(form):
            pass
            
        local_defs = list(locals().items())
        for name, func in local_defs:
            
            if name == form.auth_method.data:
                func(form)
                break
        
        
        
        return redirect(url_for("creds.credentials"))

    return render_template("index.html", page=page, form=form,
                           title=title, func=func, action_url=action_url)

