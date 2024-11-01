from flask import Blueprint, render_template, abort, flash, session, redirect, url_for
from flask_login import login_required
import os
import pathlib


from app import db
from app.forms import UserForm
from app.models import Users, SuperUser, LicensesUsers

path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
admin = Blueprint("admin", __name__, template_folder=path_template)


@admin.route("/users", methods=["GET"])
@login_required
def users():

    try:
        user = Users.query.filter(Users.login == session["login"]).first()
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
        return render_template("index.html", page=page, database=database)

    except Exception as e:
        abort(500, description=f"Erro interno do servidor: {str(e)}")


@admin.route("/cadastro/usuario", methods=["GET", "POST"])
@login_required
def cadastro_user():

    try:

        title = "Editar Usuário"
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

            form = UserForm(
                tipoUsr=("supersu", "Super Administrador"), licenses=licenses
            )

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

        return render_template("index.html", page=page, form=form, title=title)

    except Exception as e:
        abort(500, description=f"Erro interno do servidor: {str(e)}")


@admin.route("/editar/usuario/<id>", methods=["GET", "POST"])
@login_required
def edit_usuario(id: int):

    try:

        title = "Cadastro Usuário"
        form = UserForm()
        page = "FormUsr.html"

        return render_template("index.html", page=page, form=form, title=title)

    except Exception as e:
        abort(500, description=f"Erro interno do servidor: {str(e)}")


@admin.route("/deletar/usuario/<id>", methods=["GET", "POST"])
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
