from flask import Blueprint, render_template, session, url_for, redirect, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename

import os
import pathlib
from collections import Counter

from app import db
from app.forms.credentials import CredentialsForm
from app.models import Credentials, BotsCrawJUD, LicensesUsers, Users

path_template = os.path.join(pathlib.Path(
    __file__).parent.resolve(), "templates")
cred = Blueprint("creds", __name__, template_folder=path_template)


@cred.route("/credentials/dashboard", methods=["GET"])
@login_required
def credentials():
    user = Users.query.filter(Users.login == session["login"]).first()
    license_token = user.licenses[0].license_token

    database = db.session.query(LicensesUsers).\
        filter(LicensesUsers.license_token ==
               license_token).first().credentials

    title = "Credenciais"
    page = "credentials.html"
    return render_template("index.html", page=page, title=title, database=database)


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

        if Credentials.query.filter(Credentials.
                                    nome_credencial == form.
                                    nome_cred.data).first():

            flash("Existem credenciais com este nome já cadastrada!", "error")
            return redirect(url_for("creds.cadastro"))

        def pw(form):

            passwd = Credentials(
                nome_credencial=form.nome_cred.data,
                system=form.system.data,
                login_method=form.auth_method.data,
                login=form.login.data,
                password=form.password.data
            )
            db.session.add(passwd)
            licenseusr = LicensesUsers.query.filter(
                LicensesUsers.license_token == session["license_token"]).first()
            licenseusr.credentials.append(passwd)
            db.session.commit()

        def cert(form):

            temporarypath = current_app.config["TEMP_PATH"]
            filecert = form.cert.data

            cer_path = os.path.join(
                temporarypath, secure_filename(filecert.filename))
            filecert.save(cer_path)

            with open(cer_path, "rb") as f:
                certficate_blob = f.read()

            passwd = Credentials(
                nome_credencial=form.nome_cred.data,
                system=form.system.data,
                login_method=form.auth_method.data,
                login=form.doc_cert.data,
                key=form.key.data,
                certficate=filecert.filename,
                certficate_blob=certficate_blob
            )
            db.session.add(passwd)
            licenseusr = LicensesUsers.query.filter(
                LicensesUsers.license_token == session["license_token"]).first()
            licenseusr.credentials.append(passwd)
            db.session.commit()

        local_defs = list(locals().items())
        for name, func in local_defs:

            if name == form.auth_method.data:
                func(form)
                break

        flash("Credencial salva com sucesso!", "success")
        return redirect(url_for("creds.credentials"))

    return render_template("index.html", page=page, form=form,
                           title=title, func=func, action_url=action_url)


@cred.route("/credentials/editar/<id>", methods=["GET", "POST"])
@login_required
def editar(id: int = None):

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

        flash("Credencial salva com sucesso!", "success")
        return redirect(url_for("creds.credentials"))

    return render_template("index.html", page=page, form=form,
                           title=title, func=func, action_url=action_url)


@cred.route("/credentials/deletar/<id>", methods=["GET", "POST"])
@login_required
def deletar(id: int = None):

    to_delete = Credentials.query.\
        filter(Credentials.id == id).first()

    db.session.delete(to_delete)
    db.session.commit()

    message = "Credencial deletada!"

    template = "include/show.html"
    return render_template(template, message=message)
