from flask import Blueprint, render_template, request, session, jsonify
from flask_login import login_required

import os
import json
import locale
import pathlib
import pandas as pd

from datetime import datetime
from collections import Counter
from deep_translator import GoogleTranslator

from app import db
from app.models import Users, LicensesUsers, Executions, SuperUser

translator = GoogleTranslator(source="en", target="pt")

path_static = os.path.join(pathlib.Path(__file__).parent.resolve(), "static")
path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")

dash = Blueprint(
    "dash", __name__, template_folder=path_template, static_folder=path_static
)


@dash.route("/dashboard", methods=["GET"])
@login_required
def dashboard():

    title = "Dashboard"
    page = "dashboard.html"

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

    database = executions.all()

    return render_template("index.html", page=page, title=title, database=database)


@dash.route("/PerMonth", methods=["GET"])
@login_required
def perMonth():

    # Define a localidade para português do Brasil
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

    chart_data = {"labels": [], "values": []}  # Preenche com 0 se o mês estiver ausente

    admin_cookie = request.cookies.get("roles_admin")
    supersu_cookie = request.cookies.get("roles_supersu")

    if supersu_cookie and json.loads(supersu_cookie).get("login_id") == session["_id"]:
        query_result = Executions.query.all()

    elif admin_cookie and json.loads(admin_cookie).get("login_id") == session["_id"]:
        query_result = (
            db.session.query(Executions)
            .join(LicensesUsers)
            .filter(LicensesUsers.license_token == session["license_token"])
            .all()
        )

    elif not supersu_cookie or not admin_cookie:
        query_result = (
            db.session.query(Executions)
            .join(Users)
            .filter(Users.login == session["login"])
            .all()
        )

    # Extrai o mês de cada data de execução em português
    if query_result:

        meses = []
        current_year = datetime.now().year
        for execut in query_result:
            execution_date = execut.data_execucao
            if execution_date and execution_date.year == current_year:
                # Converte para o nome do mês em português
                mes_nome = execution_date.date().strftime("%B").lower()
                meses.append(mes_nome)

        # Conta as ocorrências de cada mês
        execucoes_por_mes = Counter(meses)

        # Lista completa de meses em português para garantir que todos os meses estejam representados
        all_months = [
            "janeiro",
            "fevereiro",
            "março",
            "abril",
            "maio",
            "junho",
            "julho",
            "agosto",
            "setembro",
            "outubro",
            "novembro",
            "dezembro",
        ]

        # Garante que todos os meses estejam na contagem, mesmo que com valor 0
        chart_data = {
            "labels": all_months,
            "values": [
                execucoes_por_mes.get(month, 0) for month in all_months
            ],  # Preenche com 0 se o mês estiver ausente
        }

    # Retorna para o template
    return jsonify(chart_data)


@dash.route("/MostExecuted", methods=["GET"])
@login_required
def MostExecuted():

    # Executa a query para obter todos os registros
    admin_cookie = request.cookies.get("roles_admin")
    supersu_cookie = request.cookies.get("roles_supersu")

    chart_data = {"labels": [], "values": []}

    if supersu_cookie and json.loads(supersu_cookie).get("login_id") == session["_id"]:
        query_result = Executions.query.all()

    elif admin_cookie and json.loads(admin_cookie).get("login_id") == session["_id"]:
        query_result = (
            db.session.query(Executions)
            .join(LicensesUsers)
            .filter(LicensesUsers.license_token == session["license_token"])
            .all()
        )

    elif not supersu_cookie or not admin_cookie:
        query_result = (
            db.session.query(Executions)
            .join(Users)
            .filter(Users.login == session["login"])
            .all()
        )

    if query_result:
        # Converte o query result para uma lista de dicionários
        data = [{"bot_name": execut.bot.display_name} for execut in query_result]

        # Cria o DataFrame a partir da lista de dicionários
        df = pd.DataFrame(data)

        # Agrupando pelo nome do bot e contando as execuções totais
        execucoes_por_bot = df["bot_name"].value_counts().reset_index()
        execucoes_por_bot.columns = ["bot_name", "count"]

        # Preparando dados para o Chart.js
        chart_data = {
            "labels": execucoes_por_bot["bot_name"].tolist(),
            "values": execucoes_por_bot["count"].tolist(),
        }

    # Retorna para o template
    return jsonify(chart_data)
