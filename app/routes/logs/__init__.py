from flask import (Blueprint, url_for, redirect, render_template,
                   flash, jsonify, session, request, make_response)

from flask_login import login_required

import os
import json
import pathlib
import requests

from app import db
from app.misc import generate_signed_url
from app.models import Users, Executions, LicensesUsers

path_template = os.path.join(pathlib.Path(
    __file__).parent.resolve(), "templates")
logsbot = Blueprint("logsbot", __name__, template_folder=path_template)


def stopbot(user: str, pid: str, socket: str):

    requests.post(url=f'{socket}/stop/{user}/{pid}', timeout=300)


@logsbot.context_processor
def SendPid_UrlSocket():
    
    pid = request.cookies.get('pid')
    socket_bot = request.cookies.get('socket_bot')
    
    return dict(pid=pid, socket_bot=socket_bot)


@logsbot.route('/logs_bot/<pid>')
@login_required
def logs_bot(pid: str):

    title = f"Execução {pid}"
    user_id = Users.query.filter(Users.login == session["login"]).first().id
    execution = db.session.query(Executions).join(Executions.user).filter(
        Users.id == user_id,  # Supondo que você também queira filtrar por um user_id específico
        Executions.pid == pid
    ).first()
    
    admin_cookie, supersu_cookie = None, None
    
    admin_cookie = request.cookies.get('roles_admin')
    supersu_cookie = request.cookies.get('roles_supersu')
    
    if admin_cookie and not supersu_cookie:
        if json.loads(admin_cookie).get("login_id") == session["_id"]:
            execution = db.session.query(Executions).\
                join(Users).\
                join(LicensesUsers).\
                filter(LicensesUsers.license_token == session["license_token"],
                       Executions.pid == pid).first()
    
    elif supersu_cookie:
        if json.loads(supersu_cookie).get("login_id") == session["_id"]:
            execution = Executions.query.filter(Executions.pid == pid).first()


    if execution is None:
        return redirect(f"{url_for('exe.executions')}")

    if execution.status == "Finalizado":
        return redirect(f"{url_for('exe.executions')}?pid={pid}")

    rows = execution.total_rows
    resp = make_response(render_template(
        "index.html", page='logs_bot.html', pid=pid,
        total_rows=rows, title=title))
    
    resp.set_cookie("socket_bot", execution.url_socket, max_age=60 * 60 * 24,
                    httponly=True, secure=True, samesite='Lax')
    
    resp.set_cookie("pid", pid, max_age=60 * 60 * 24,
                    httponly=True, secure=True, samesite='Lax')
    return resp


@logsbot.route('/stop_bot/<pid>', methods=["GET"])
@login_required
def stop_bot(pid: str):
    
    socket = request.cookies.get("socket_bot")
    stopbot(session["login"], pid, socket)
    flash("Execução encerrada", "success")
    return redirect(url_for("exe.executions"))


@logsbot.route('/status/<pid>', methods=["GET"])
@login_required
def status(pid):

    response_data = {"erro": "erro"}
    user_id = Users.query.filter(Users.login == session["login"]).first().id
    execution = db.session.query(Executions).join(Executions.user).filter(
        Users.id == user_id,  # Supondo que você também queira filtrar por um user_id específico
        Executions.pid == pid
    ).first()
    
    admin_cookie, supersu_cookie = None, None
    
    admin_cookie = request.cookies.get('roles_admin')
    supersu_cookie = request.cookies.get('roles_supersu')
    
    if admin_cookie and not supersu_cookie:
        if json.loads(admin_cookie).get("login_id") == session["_id"]:
            execution = db.session.query(Executions).\
                join(Users).\
                join(LicensesUsers).\
                filter(LicensesUsers.license_token == session["license_token"],
                       Executions.pid == pid).first()
    
    elif supersu_cookie:
        if json.loads(supersu_cookie).get("login_id") == session["_id"]:
            execution = Executions.query.filter(Executions.pid == pid).first()
    
    if execution.status and execution.status == "Finalizado":
        signed_url = generate_signed_url(execution.file_output)
        response_data = {
            "message": "OK",
            "document_url": signed_url
        }
        return jsonify(response_data), 200
    
    return jsonify(response_data), 500
