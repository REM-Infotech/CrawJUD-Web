from flask import Blueprint, render_template, abort, flash, session, request
from flask_login import login_required
import os
import pathlib


from app import db
from app.forms import UserForm
from app.models import Users, SuperUser, LicensesUsers

path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
admin = Blueprint("admin", __name__, template_folder=path_template)


@admin.route('/users', methods=["GET"])
@login_required
def users():

    try:
        user = Users.query.filter(Users.login == session["login"]).first()
        user_id = user.id

        chksupersu = db.session.query(SuperUser).join(
            Users).filter(Users.id == user_id).first()

        users = db.session.query(Users)
        if not chksupersu:

            users = users.join(LicensesUsers).\
                filter_by(license_token=user.licenseusr.license_token)

        database = users.all()

        page = "users.html"
        return render_template("index.html", page=page, database=database)

    except Exception as e:
        abort(500, description=f"Erro interno do servidor: {str(e)}")


@admin.route('/cadastro/usuario', methods=["GET", "POST"])
@login_required
def cadastro_user():

    try:

        title = "Cadastro Usuário"
        form = UserForm()
        page = "FormUsr.html"

        return render_template("index.html", page=page, form=form, title=title)

    except Exception as e:
        abort(500, description=f"Erro interno do servidor: {str(e)}")


@admin.route('/editar/usuario/<id>', methods=["GET", "POST"])
@login_required
def edit_usuario(id: int):

    try:

        title = "Editar Usuário"
        form = UserForm()
        page = "FormUsr.html"
        
        flash("Hello World!", "success")
        return render_template("index.html", page=page, form=form, title=title)
    
    except Exception as e:
        abort(500, description=f"Erro interno do servidor: {str(e)}")


@admin.route('/deletar/usuario/<id>', methods=["GET", "POST"])
@login_required
def delete_usuario(id: int):
    
    try:
        
        title = "Editar Usuário"
        form = UserForm()
        page = "FormUsr.html"
        
        flash("Hello World!", "success")
        return render_template("index.html", page=page, form=form, title=title)
    
    except Exception as e:
        abort(500, description=f"Erro interno do servidor: {str(e)}")
