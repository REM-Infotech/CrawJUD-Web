from flask import Blueprint, render_template, session, request
from flask_login import login_required

import os
import pathlib

from app import db
from app.forms import SearchExec
from app.models import Executions, Users, LicensesUsers, SuperUser
from sqlalchemy.orm import aliased
path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
exe = Blueprint("exe", __name__, template_folder=path_template)

@exe.route("/executions", methods = ["GET", "POST"])
@login_required
def executions():
    
    try:
        form = SearchExec()
        pid = ""
        if form.validate_on_submit():
            pid = form.campo_busca.data
        user = Users.query.filter(Users.login == session["login"]).first()
        user_id = user.id
        
        chksupersu = db.session.query(SuperUser).join(
            Users).filter(Users.id == pid).first()
        
        executions = db.session.query(Executions)
        if not chksupersu:
            
            license_token = user.licenses[0].license_token
            
            join_admins = executions.join(
                Executions.licenses).join(LicensesUsers.admins).filter(Users.id == "user_id")
            
            admin_result = join_admins.first()
            
            executions = executions.join(
                Executions.licenses).filter(
                LicensesUsers.license_token == license_token)
  
            if not admin_result:
                executions = executions.join(
                    LicensesUsers.users).filter(Users.id == user_id)
                
            if pid:
                executions = executions.filter(Executions.pid.contains(pid))
        database = executions.all()
        
    except Exception as e:
        print(f"Error occurred: {e}")


    title = "Execuções"
    page = "executions.html"
    return render_template("index.html", page=page, title=title, 
                           database =database, form=form)   
