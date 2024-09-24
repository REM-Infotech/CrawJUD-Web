from app import db
from app import app

from app.models.users import Users, LicensesUsers
from app.models.bots import BotsCrawJUD

import pandas as pd
from uuid import uuid4

def init_database():
    
    with app.app_context():
        
        db.create_all()
        
        dbase = Users.query.filter(Users.login == "root").first()
        if not dbase:
            
            senha = str(uuid4())
            
            user = Users(
                login="root",
                nome_usuario="Root",
                email="nicholas@robotz.dev",
                license_key=str(uuid4()))
            user.senhacrip = senha
            
            license_user = LicensesUsers(
                name_client="Robotz Dev",
                cpf_cnpj="55607848000175",
                email_admin="nicholas@robotz.dev",
                license_token=str(uuid4()),
                user=user
            )
            df = pd.read_excel(r"C:\Users\nicholas.silva\Documents\Github\CrawJUD-Web\export.xlsx")
            df.columns = df.columns.str.lower()

            data = []
            for _, row in df.iterrows():
                data_append = {}
                row = row.dropna()
                data_info = row.to_dict()
                for coluna in BotsCrawJUD.__table__.columns:
                    item = data_info.get(coluna.name, None)
                    if item:
                        data_append.update({coluna.name: item})

                    elif not item:

                        if coluna.name == "id":
                            continue
                        data_append.update({coluna.name: "Sem Informação"})

                appends = BotsCrawJUD(**data_append)
                data.append(appends)
            
            
            db.session.add(user)
            db.session.add(license_user)
            db.session.add_all(data)
            db.session.commit()
            
            print(f" * Root Pw: {senha}")
        
        