from flask import Blueprint, url_for, redirect, render_template, flash, jsonify, session
from flask_login import login_required
from flask_sqlalchemy.query import Query

import os
import pathlib
import requests
from typing import Type

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
    
    if not "https://" in url:
        url = "https://" + url
    
    return url


def obter_status_bot(pid: str) -> Type[Query]:

    return 'ExecutionsTable.query.filter_by(pid=pid, status="Finalizado").first()'


def stopbot(user: str, pid: str, socket: str):

    requests.post(url=f'{socket}/stop/{user}/{pid}', timeout=30)

@logsbot.route('/logs_bot/<sid>')
@login_required
def logs_bot(sid: str):

    user_id = Users.query.filter(Users.login == session["login"]).first().id
    execution = db.session.query(Executions).join(Executions.user).filter(
        Users.id == user_id,  # Supondo que você também queira filtrar por um user_id específico
        Executions.pid == sid
    ).first()
    
    if execution is None:

        return redirect(url_for('exe.executions'))

    if execution.status == "Finalizado":
        return redirect(url_for('exe.executions'))

    rows = execution.total_rows
    return render_template("index.html", page='logs_bot.html', pid=sid, total_rows=rows, titlehtml=f"Execução - {sid}")


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
