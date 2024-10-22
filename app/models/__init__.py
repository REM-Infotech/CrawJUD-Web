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
        passwd  = values.get("passwd", str(uuid4()))
        
        dbase = Users.query.filter(Users.login == loginsys).first()
        if not dbase:

            user = Users(
                login=loginsys,
                nome_usuario=nomeusr,
                email=emailusr)
            user.senhacrip = passwd
            
            license_user = LicensesUsers.query.filter(
                LicensesUsers.name_client=="Robotz Dev"
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
                    appends = BotsCrawJUD(**values)
                    license_user.bots.append(appends)
                    data.append(appends)
            
            
            db.session.add(user)
            db.session.add_all(data)
            db.session.add(license_user)
            db.session.commit()
            
            print(f" * Root Pw: {passwd}")
        
def setServer(args):
    
    pass