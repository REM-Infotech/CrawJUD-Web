from flask import Blueprint, url_for, redirect, render_template, flash, jsonify, session
from flask_login import login_required

import os
import pathlib
import requests

from app import db
from app.misc import generate_signed_url
from app.models import Users, Executions

path_template = os.path.join(pathlib.Path(
    __file__).parent.resolve(), "templates")
logsbot = Blueprint("logsbot", __name__, template_folder=path_template)


def obter_endereco_socket(user: str, pid: str) -> str:

    user_id = Users.query.filter(Users.login == session["login"]).first().id
    execution = db.session.query(Executions).join(Executions.user).filter(
        Users.id == user_id,  # Supondo que você também queira filtrar por um user_id específico
        Executions.pid == pid
    ).first()
    
    url = f"{execution.url_socket}"
    
    if "https://" not in url:
        url = "https://" + url
    
    return url


def stopbot(user: str, pid: str, socket: str):

    requests.post(url=f'{socket}/stop/{user}/{pid}', timeout=300)


@logsbot.route('/logs_bot/<sid>')
@login_required
def logs_bot(sid: str):

    title = f"Execução {sid}"
    user_id = Users.query.filter(Users.login == session["login"]).first().id
    execution = db.session.query(Executions).join(Executions.user).filter(
        Users.id == user_id,  # Supondo que você também queira filtrar por um user_id específico
        Executions.pid == sid
    ).first()
    
    if execution is None:

        return redirect(f"{url_for('exe.executions')}?pid={sid}")

    if execution.status == "Finalizado":
        return redirect(f"{url_for('exe.executions')}?pid={sid}")

    rows = execution.total_rows
    return render_template("index.html", page='logs_bot.html', pid=sid,
                           total_rows=rows, title=title)


@logsbot.route('/socket_address/<pid>', methods=["GET"])
@login_required
def socket_address(pid: str):

    socket = obter_endereco_socket(session["login"], pid)
    session["socket"] = socket
    return socket


@logsbot.route('/stop_bot/<pid>', methods=["GET"])
@login_required
def stop_bot(pid: str):

    socket: str = obter_endereco_socket(session["login"], pid)
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
    
    if execution.status and execution.status == "Finalizado":
        signed_url = generate_signed_url(execution.file_output)
        response_data = {
            "message": "OK",
            "document_url": signed_url
        }
        return jsonify(response_data), 200
    
    return jsonify(response_data), 500
