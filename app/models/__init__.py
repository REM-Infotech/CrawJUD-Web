from flask import current_app
from app import db

from app.models.secondaries import(admins, execution_bots, 
execution_licenses, execution_users, licenses_users_bots, licenseusr, 
licenses_users_credentials)
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
                
            license_user.users.append(user)
            license_user.admins.append(user)
            super_user = SuperUser()
            
            super_user.users = user
            
            df = pd.read_excel("export.xlsx")
            df.columns = df.columns.str.lower()

            data = []
            for _, row in df.iterrows():
                data_append = {}
                row = row.dropna()
                data_info = row.to_dict()
                for coluna in BotsCrawJUD.__table__.columns:
                    item = data_info.get(coluna.name, None)
                    if item:
                        if coluna.name == "id":
                            continue
                        data_append.update({coluna.name: item})

                    elif not item:

                        if coluna.name == "id":
                            continue
                        data_append.update({coluna.name: "Sem Informação"})

                appends = BotsCrawJUD(**data_append)
                license_user.bots.append(appends)
                data.append(appends)
            
            
            db.session.add(user)
            db.session.add_all(data)
            db.session.add(license_user)
            db.session.commit()
            
            print(f" * Root Pw: {passwd}")
        
def setServer(args):
    
    pass