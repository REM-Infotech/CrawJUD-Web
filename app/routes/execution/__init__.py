import os
import pathlib

from flask import (
    Blueprint,
    Response,
    abort,
    make_response,
    redirect,
    render_template,
    request,
    session,
)
from flask_login import login_required
from sqlalchemy.orm import aliased

from app import db
from app.forms import SearchExec
from app.misc import generate_signed_url
from app.models import Executions, SuperUser, Users, admins

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

        chksupersu = (
            db.session.query(SuperUser)
            .select_from(Users)
            .join(Users.supersu)
            .filter(Users.login == session["login"])
            .first()
        )

        executions = db.session.query(Executions)

        if chksupersu:

            alias = aliased(
                Users,
                (
                    db.session.query(Users)
                    .filter(Users.login == session["login"])
                    .subquery()
                ),
            )

            executions = executions.join(
                alias, Executions.license_id == alias.licenseus_id
            )

            chk_admin = (
                db.session.query(admins)
                .join(alias, admins.c.users_id == alias.id)
                .filter(admins.c.license_user_id == alias.licenseus_id)
                .first()
            )

            if not chk_admin:
                executions = executions.join(alias, Executions.user_id == alias.id)

        executions = executions.filter(Executions.pid.contains(pid))
        database = executions.all()

    except Exception:
        abort(500)

    title = "Execuções"
    page = "executions.html"
    return make_response(
        render_template(
            "index.html", page=page, title=title, database=database, form=form
        )
    )


@exe.route("/executions/download/<filename>")
@login_required
def download_file(filename: str) -> Response:

    signed_url = generate_signed_url(filename)

    # Redireciona para a URL assinada
    return make_response(redirect(signed_url))
