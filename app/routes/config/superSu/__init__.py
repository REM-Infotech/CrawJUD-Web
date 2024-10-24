from flask import Blueprint, render_template, abort
from flask_login import login_required
import os
import pathlib

path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
supersu = Blueprint("supersu", __name__, template_folder=path_template)

@supersu.route('/configurações', methods=["GET"])
@login_required
def config():
    
    try:
        return render_template("index.html")
    
    except Exception as e:
        abort(500)

@supersu.route('/cadastro/usuario', methods=["GET", "POST"])
@login_required
def cadastro_user():
    
    try:
        return render_template("index.html")
    
    except Exception as e:
        abort(500)

@supersu.route('/editar/usuario', methods=["GET", "POST"])
@login_required
def edit_usuario():
    
    try:
        return render_template("index.html")
    
    except Exception as e:
        abort(500)

