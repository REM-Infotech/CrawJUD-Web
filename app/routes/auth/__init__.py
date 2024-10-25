from flask import (Blueprint, render_template, redirect,
                   url_for, flash, session, request)
from flask_login import login_user, logout_user
import os
import pathlib

from app.forms.auth.login import LoginForm
from app.models.users import Users

path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
auth = Blueprint("auth", __name__, template_folder=path_template)



@auth.before_request
def nexturl():
    
    if request.args.get("next"):
        session["location"] = request.args.get("next")


@auth.route("/login", methods=["GET", "POST"])
def login():
    
    form = LoginForm()
    
    if form.validate_on_submit():
        
        usr = Users.query.filter(Users.login == form.login.data).first()
        if usr is None or not usr.check_password(form.password.data):
            
            flash("Senha incorreta!", "error")
            return redirect(url_for("auth.login"))
        
        
        if not session.get("location"):
            session["location"] = url_for("dash.dashboard")
        
        license_usr = usr.licenseusr
        session.permanent = form.remember_me.data
        
        if usr.admin:
            session["admin"] = "True"
            
        if usr.supersu:
            session["supersu"] = "True"
            
        session["login"] = usr.login
        session["nome_usuario"] = usr.nome_usuario
        session["license_token"] = license_usr.license_token
        login_user(usr, remember=form.remember_me.data)
        flash("Login efetuado com sucesso!", "success")
        return redirect(session["location"])
    
    return render_template("login.html", form=form)


@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    return ""


@auth.route("/logout", methods=["GET", "POST"])
def logout():
    
    logout_user()
    if session.get("location"):
        session.pop('location')
        
    flash("Logout efetuado com sucesso!", "success")
    return redirect(url_for("auth.login"))
