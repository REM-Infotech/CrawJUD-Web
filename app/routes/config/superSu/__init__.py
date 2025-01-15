import os
import pathlib

from flask import Blueprint, abort, render_template
from flask_login import login_required

from ....decorators import checkSu

path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
supersu = Blueprint("supersu", __name__, template_folder=path_template)


@supersu.route("/configurações_crawjud", methods=["GET"])
@login_required
@checkSu
def config() -> str:

    try:
        return render_template("index.html")

    except Exception as e:
        abort(500, description=f"Erro interno do servidor: {str(e)}")


@supersu.route("/cadastro/cliente", methods=["GET", "POST"])
@login_required
@checkSu
def cadastro_cliente() -> str:

    try:
        return render_template("index.html")

    except Exception as e:
        abort(500, description=f"Erro interno do servidor: {str(e)}")


@supersu.route("/editar/cliente", methods=["GET", "POST"])
@login_required
@checkSu
def edit_cliente() -> str:

    try:
        return render_template("index.html")

    except Exception as e:
        abort(500, description=f"Erro interno do servidor: {str(e)}")
