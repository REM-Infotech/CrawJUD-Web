import os
import pathlib

from flask import Blueprint, redirect, render_template, request, session
from flask_login import login_required

from app import db
from app.forms import SearchExec
from app.misc import generate_signed_url
from app.models import Executions, LicensesUsers, SuperUser, Users

path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
exe = Blueprint("exe", __name__, template_folder=path_template)


@exe.route("/executions", methods=["GET", "POST"])
@login_required
def executions():

    try:
        form = SearchExec()
        pid = request.args.get("pid", "")

        if form.validate_on_submit():
            pid = form.campo_busca.data

        user = Users.query.filter(Users.login == session["login"]).first()
        user_id = user.id

        chksupersu = (
            db.session.query(SuperUser).join(Users).filter(Users.id == user_id).first()
        )

        executions = db.session.query(Executions)
        if not chksupersu:

            executions = executions.join(LicensesUsers).filter_by(
                license_token=user.licenseusr.license_token
            )

            chk_admin = (
                db.session.query(LicensesUsers)
                .join(LicensesUsers.admins)
                .filter(Users.id == user_id)
                .first()
            )

            if not chk_admin:
                executions = executions.join(Users).filter(Users.id == user_id)

        executions = executions.filter(Executions.pid.contains(pid))
        database = executions.all()

    except Exception as e:
        print(f"Error occurred: {e}")

    title = "Execuções"
    page = "executions.html"
    return render_template(
        "index.html", page=page, title=title, database=database, form=form
    )


@exe.route("/executions/download/<filename>")
@login_required
def download_file(filename: str):

    signed_url = generate_signed_url(filename)

    # Redireciona para a URL assinada
    return redirect(signed_url)
