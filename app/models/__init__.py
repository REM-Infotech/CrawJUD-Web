from flask import current_app
from app import db

from app.models.secondaries import admins, execution_bots
from app.models.users import Users, LicensesUsers, SuperUser
from app.models.bots import BotsCrawJUD, Credentials, Executions
from app.models.srv import Servers

import pandas as pd
from uuid import uuid4
from dotenv import dotenv_values


def init_database():
    app = current_app
    with app.app_context():
        
        values = dotenv_values()
        db.create_all()
        loginsys = values.get("loginsys")
        nomeusr = values.get("nomeusr")
        emailusr = values.get("emailusr")
        passwd = values.get("passwd", str(uuid4()))
        
        dbase = Users.query.filter(Users.login == loginsys).first()
        if not dbase:

            user = Users(
                login=loginsys,
                nome_usuario=nomeusr,
                email=emailusr)
            user.senhacrip = passwd
            
            license_user = LicensesUsers.query.filter(
                LicensesUsers.name_client == "Robotz Dev"
            ).first()
            
            if not license_user:
            
                license_user = LicensesUsers(
                    name_client="Robotz Dev",
                    cpf_cnpj="55607848000175",
                    license_token=str(uuid4()),
                )
                
            user.licenseusr = license_user
            license_user.admins.append(user)
            super_user = SuperUser()
            
            super_user.users = user
            
            df = pd.read_excel("export.xlsx")
            df.columns = df.columns.str.lower()

            data = []
            for values in list(df.to_dict(orient="records")):
                
                key = list(values)[1]
                value = values.get(key)
                
                chk_bot = BotsCrawJUD.query.filter_by(
                            **{key: value}).first()
                
                if not chk_bot:
                    appends = BotsCrawJUD()
                    
                    for key, var in values.items():
                        appends.__dict__.update({key: var})
                        
                    license_user.bots.append(appends)
                    data.append(appends)
            
            
            db.session.add(user)
            db.session.add_all(data)
            db.session.add(license_user)
            db.session.commit()
            
            print(f" * Root Pw: {passwd}")
    
    
    license_user = LicensesUsers.query.filter(
                LicensesUsers.name_client == "Fonseca Melo Viana"
    ).first()
    
    if not license_user:
        license_user = LicensesUsers(
            name_client="Fonseca Melo Viana",
            cpf_cnpj="11594617000107",
            license_token=str(uuid4()))

        with db.session.no_autoflush:
            
            df = pd.read_excel("export.xlsx")
            df.columns = df.columns.str.lower()
            data = []
            db.session.add(license_user)
            for values in list(df.to_dict(orient="records")):
                
                key = list(values)[1]
                value = values.get(key)
                
                chk_bot = BotsCrawJUD.query.filter_by(
                            **{key: value}).first()
                
                if chk_bot not in license_user.bots:
                    license_user.bots.append(chk_bot)

            df = pd.read_excel("export2.xlsx")
            df.columns = df.columns.str.lower()
            to_add_usr = []
            for value in list(df.to_dict(orient="records")):

                chk_usr = Users.query.filter_by(**{"login": value.get("login")}).first()
                if not chk_usr:
                    add_usr = Users()
                    for key, var in value.items():
                        if key == admins and var:
                            license_user.admins.append(user)
                            
                        add_usr.__dict__.update({key: var})
                    
                    add_usr.licenseusr = license_user
                    to_add_usr.append(add_usr)
                elif chk_usr:
                    chk_usr.licenseusr = license_user
                    
            if len(to_add_usr) > 0:
                db.session.add_all(to_add_usr)
                
            db.session.commit()
