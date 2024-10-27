from flask import Blueprint, render_template, request, session, jsonify
from flask_login import login_required

import os
import json
import pathlib
import calendar

import pandas as pd
from deep_translator import GoogleTranslator

from app import db
from app.models import Users, LicensesUsers, Executions

translator = GoogleTranslator(source="en", target="pt")

path_static = os.path.join(pathlib.Path(__file__).parent.resolve(), "static")
path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")

dash = Blueprint("dash", __name__, template_folder=path_template, static_folder=path_static)


@dash.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    
    title = "Dashboard"
    page = "dashboard.html"
    return render_template("index.html", page=page, title=title)


@dash.route("/PerMonth", methods=["GET"])
@login_required
def perMonth():
    
    admin_cookie = request.cookies.get('roles_admin')
    supersu_cookie = request.cookies.get('roles_supersu')
    
    if supersu_cookie and json.loads(supersu_cookie).get("login_id") == session["_id"]:
        query_result = Executions.query.all()
    
    elif admin_cookie and json.loads(admin_cookie).get("login_id") == session["_id"]:
        query_result = db.session.query(Executions).\
            join(LicensesUsers).\
            filter(LicensesUsers.license_token == session["license_token"]).all()

    elif not supersu_cookie or not admin_cookie:
        query_result = db.session.query(Executions).\
            join(Users).\
            filter(Users.login == session["login"]).all()
    
    # Converte o query result para uma lista de dicionários
    data = [{'bot_name': execut.bot.display_name, 'execution_date': execut.data_execucao}
            for execut in query_result]
    
    # Cria o DataFrame a partir da lista de dicionários
    df = pd.DataFrame(data)

    # Transformando a coluna para datetime
    df['execution_date'] = pd.to_datetime(df['execution_date'])
    df['month'] = df['execution_date'].dt.to_period('M')

    # Contagem de execuções por mês
    execucoes_por_mes = df.groupby('month').size()
    execucoes_por_mes = execucoes_por_mes.reset_index(name='count')

    execucoes_por_mes['month'] = execucoes_por_mes['month'].apply(
    lambda x: calendar.month_name[int(x)] if isinstance(x, (int, str)) and str(x).isdigit() else x)
    execucoes_por_mes['month'].apply(lambda x: translator.translate(x))
    
    # Convertendo para JSON
    chart_data = {
        "labels": execucoes_por_mes['month'].astype(str).tolist(),  # Converte os períodos para string
        "data": execucoes_por_mes['count'].tolist()  # Quantidade de execuções
    }

    # Retorna para o template
    return jsonify(chart_data)


@dash.route("/MostExecuted", methods=["GET"])
@login_required
@login_required
def MostExecuted():
    
    # Executa a query para obter todos os registros
    admin_cookie = request.cookies.get('roles_admin')
    supersu_cookie = request.cookies.get('roles_supersu')
    
    if supersu_cookie and json.loads(supersu_cookie).get("login_id") == session["_id"]:
        query_result = Executions.query.all()
    
    elif admin_cookie and json.loads(admin_cookie).get("login_id") == session["_id"]:
        query_result = db.session.query(Executions).\
            join(LicensesUsers).\
            filter(LicensesUsers.license_token == session["license_token"]).all()

    elif not supersu_cookie or not admin_cookie:
        query_result = db.session.query(Executions).\
            join(Users).\
            filter(Users.login == session["login"]).all()
    
    # Converte o query result para uma lista de dicionários
    data = [{'bot_name': execut.bot.display_name}
            for execut in query_result]
    
    # Cria o DataFrame a partir da lista de dicionários
    df = pd.DataFrame(data)
    
    # Agrupando pelo nome do bot e contando as execuções totais
    execucoes_por_bot = df['bot_name'].value_counts().reset_index()
    execucoes_por_bot.columns = ['bot_name', 'count']

    # Preparando dados para o Chart.js
    chart_data = {
        "labels": execucoes_por_bot['bot_name'].tolist(),
        "data": execucoes_por_bot['count'].tolist()
    }

    # Retorna para o template
    return jsonify(chart_data)
