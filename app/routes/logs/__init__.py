import json
import os
import pathlib
from time import sleep

from flask_sqlalchemy import SQLAlchemy
import httpx as requests
from flask import (
    Blueprint,
    Response,
    abort,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_required
from flask import current_app as app
from app.misc import generate_signed_url
from app.models import Executions, LicensesUsers, Users

path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
logsbot = Blueprint("logsbot", __name__, template_folder=path_template)


def stopbot(user: str, pid: str, socket: str) -> None:

    requests.post(url=f"{socket}/stop/{user}/{pid}", timeout=300)


@logsbot.context_processor
def SendPid_UrlSocket() -> dict[str, str | None]:

    pid = request.cookies.get("pid")
    socket_bot = request.cookies.get("socket_bot")

    return dict(pid=pid, socket_bot=socket_bot)


@logsbot.route("/logs_bot/<pid>")
@login_required
def logs_bot(pid: str) -> Response:

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    if not session.get("license_token"):

        flash("Sessão expirada. Faça login novamente.", "error")
        return make_response(redirect(url_for("auth.login")))

    title = f"Execução {pid}"
    user_id = Users.query.filter(Users.login == session["login"]).first().id
    execution = (
        db.session.query(Executions)
        .join(Users, Users.id == user_id)
        .filter(Executions.pid == pid)
        .first()
    )

    admin_cookie, supersu_cookie = None, None

    admin_cookie = request.cookies.get("roles_admin")
    supersu_cookie = request.cookies.get("roles_supersu")

    if admin_cookie and not supersu_cookie:
        if json.loads(admin_cookie).get("login_id") == session["_id"]:
            execution = (
                db.session.query(Executions)
                .join(Users)
                .join(LicensesUsers)
                .filter(
                    LicensesUsers.license_token == session["license_token"],
                    Executions.pid == pid,
                )
                .first()
            )

    elif supersu_cookie:
        if json.loads(supersu_cookie).get("login_id") == session["_id"]:
            execution = Executions.query.filter(Executions.pid == pid).first()

    if execution is None:
        return make_response(redirect(f"{url_for('exe.executions')}"))

    if execution.status == "Finalizado":
        return make_response(redirect(f"{url_for('exe.executions')}?pid={pid}"))

    rows = execution.total_rows
    resp = make_response(
        render_template(
            "index.html", page="logs_bot.html", pid=pid, total_rows=rows, title=title
        )
    )

    resp.set_cookie(
        "socket_bot",
        execution.url_socket,
        max_age=60 * 60 * 24,
        httponly=True,
        secure=True,
        samesite="Lax",
    )

    resp.set_cookie(
        "pid", pid, max_age=60 * 60 * 24, httponly=True, secure=True, samesite="Lax"
    )
    return resp


@logsbot.route("/stop_bot/<pid>", methods=["GET"])
@login_required
def stop_bot(pid: str) -> Response:

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    socket = request.cookies.get("socket_bot")
    stopbot(session["login"], pid, f"https://{socket}")

    isStopped = True

    while isStopped:

        execut = db.session.query(Executions).filter(Executions.pid == pid).first()

        if str(execut.status).lower() == "finalizado":
            isStopped = False

        sleep(2)

    flash("Execução encerrada", "success")
    return make_response(redirect(url_for("exe.executions")))


@logsbot.route("/status/<pid>", methods=["GET"])
@login_required
def status(pid) -> Response:

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    i = 0
    if not session.get("license_token"):

        abort(405, description="Sessão expirada. Faça login novamente.")

    response_data = {"erro": "erro"}

    while i <= 5:
        user_id = Users.query.filter(Users.login == session["login"]).first().id
        execution = (
            db.session.query(Executions)
            .join(Users, Users.id == user_id)
            .filter(
                Executions.pid == pid,
            )
            .first()
        )

        admin_cookie, supersu_cookie = None, None

        admin_cookie = request.cookies.get("roles_admin")
        supersu_cookie = request.cookies.get("roles_supersu")

        if admin_cookie and not supersu_cookie:
            if json.loads(admin_cookie).get("login_id") == session["_id"]:
                execution = (
                    db.session.query(Executions)
                    .join(Users)
                    .join(LicensesUsers)
                    .filter(
                        LicensesUsers.license_token == session["license_token"],
                        Executions.pid == pid,
                    )
                    .first()
                )

        elif supersu_cookie:
            if json.loads(supersu_cookie).get("login_id") == session["_id"]:
                execution = (
                    db.session.query(Executions).filter(Executions.pid == pid).first()
                )

        if execution.status and execution.status == "Finalizado":
            signed_url = generate_signed_url(execution.file_output)
            response_data = {"message": "OK", "document_url": signed_url}
            return make_response(jsonify(response_data), 200)

        sleep(1.5)
        i += 1

    return make_response(jsonify(response_data), 500)


@logsbot.route("/url_server/<pid>", methods=["GET"])
@login_required
def url_server(pid) -> Response:

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    execution = db.session.query(Executions).filter(Executions.pid == pid).first()
    return make_response(jsonify({"url_server": execution.url_socket}))
