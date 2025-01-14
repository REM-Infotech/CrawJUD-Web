import os
import pathlib

from flask import Blueprint, Response, abort
from flask import current_app as app
from flask import flash, make_response, redirect, render_template, session, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy

from app.forms import UserForm
from app.models import LicensesUsers, SuperUser, Users

path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
admin = Blueprint("admin", __name__, template_folder=path_template)


@admin.route("/users", methods=["GET"])
@login_required
def users() -> Response:

    try:

        db: SQLAlchemy = app.extensions["sqlalchemy"]

        user = db.session.query(Users).filter(Users.login == session["login"]).first()
        user_id = user.id

        chksupersu = (
            db.session.query(SuperUser).join(Users).filter(Users.id == user_id).first()
        )

        users = db.session.query(Users)
        if not chksupersu:

            users = users.join(LicensesUsers).filter_by(
                license_token=user.licenseusr.license_token
            )

        database = users.all()

        page = "users.html"
        return make_response(
            render_template("index.html", page=page, database=database)
        )

    except Exception as e:
        abort(500, description=f"Erro interno do servidor: {str(e)}")


@admin.route("/cadastro/usuario", methods=["GET", "POST"])
@login_required
def cadastro_user() -> Response:

    try:

        db: SQLAlchemy = app.extensions["sqlalchemy"]
        if not session.get("license_token"):

            flash("Sessão expirada. Faça login novamente.", "error")
            return redirect(url_for("auth.login"))

        title = "Cadastro Usuário"
        form = UserForm()
        page = "FormUsr.html"

        user = Users.query.filter(Users.login == session["login"]).first()
        user_id = user.id

        chksupersu = (
            db.session.query(SuperUser).join(Users).filter(Users.id == user_id).first()
        )

        if chksupersu:

            licenses = []
            licenses_result = LicensesUsers.query.all()

            for lcs in licenses_result:
                licenses.append((str(lcs.license_token), str(lcs.name_client)))

            form = UserForm(licenses_add=licenses_result)

        if form.validate_on_submit():

            user = Users(
                login=form.login.data,
                nome_usuario=form.nome_usuario.data,
                email=form.email.data,
            )

            license_token = session["license_token"]
            tipo_user = form.tipo_user.data

            if chksupersu:
                if any(tipo_user == tipo for tipo in ["default_user", "admin"]):
                    license_token = form.licenses.data

                elif tipo_user == "supersu":
                    super_user = SuperUser()
                    super_user.users = user

            query_license = LicensesUsers.query.filter(
                LicensesUsers.license_token == license_token
            ).first()

            user.licenseusr = query_license

            if tipo_user == "admin":
                query_license.admins.append(user)

            user.senhacrip = form.password.data

            db.session.add(user)
            db.session.commit()

            flash("Usuário cadastrado!", "success")
            return redirect(url_for("admin.users"))

        form_items = list(form)
        for field in form_items:

            for error in field.errors:
                flash(f"Erro: {error}. Campo: {field.label.text}", "error")

        return make_response(
            render_template("index.html", page=page, form=form, title=title)
        )

    except Exception as e:
        abort(500, description=f"Erro interno do servidor: {str(e)}")


@admin.route("/editar/usuario/<id>", methods=["GET", "POST"])
@login_required
def edit_usuario(id: int) -> Response:

    try:

        db: SQLAlchemy = app.extensions["sqlalchemy"]
        if not session.get("license_token"):

            flash("Sessão expirada. Faça login novamente.", "error")
            return redirect(url_for("auth.login"))

        title = "Editar Usuário"

        user = db.session.query(Users).filter(Users.id == id).first()

        form = UserForm(**user.dict_query)
        page = "FormUsr.html"

        chksupersu = (
            db.session.query(SuperUser)
            .join(Users)
            .filter(Users.login == session["login"])
            .first()
        )

        if form.validate_on_submit():
            pass

        if chksupersu:

            licenses_result = db.session.query(LicensesUsers).all()

            form = UserForm(
                licenses_add=licenses_result,
                **user.dict_query,
            )

        return make_response(
            render_template("index.html", page=page, form=form, title=title)
        )

    except Exception as e:
        abort(500, description=f"Erro interno do servidor: {str(e)}")


@admin.route("/deletar/usuario/<id>", methods=["GET", "POST"])
@login_required
def delete_usuario(id: int) -> Response:

    try:

        title = "Editar Usuário"
        form = UserForm()
        page = "FormUsr.html"

        flash("Hello World!", "success")
        return make_response(
            render_template("index.html", page=page, form=form, title=title)
        )

    except Exception as e:
        abort(500, description=f"Erro interno do servidor: {str(e)}")
