import os
from pathlib import Path
from uuid import uuid4

import pandas as pd
from dotenv import dotenv_values
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.models.bots import BotsCrawJUD, Credentials, Executions
from app.models.secondaries import admins, execution_bots
from app.models.srv import Servers
from app.models.users import LicensesUsers, SuperUser, Users

__all__ = [
    admins,
    execution_bots,
    Users,
    LicensesUsers,
    SuperUser,
    BotsCrawJUD,
    Credentials,
    Executions,
    Servers,
]


def init_database(app: Flask, db: SQLAlchemy) -> str:

    try:
        values = dotenv_values()
        db.create_all()
        loginsys = values.get("loginsys")
        nomeusr = values.get("nomeusr")
        emailusr = values.get("emailusr")
        passwd = values.get("passusr")

        dbase = Users.query.filter(Users.login == loginsys).first()
        if not dbase:

            user = Users(login=loginsys, nome_usuario=nomeusr, email=emailusr)
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

            df = pd.read_excel(
                os.path.join(Path(__file__).parent.resolve(), "export.xlsx")
            )
            df.columns = df.columns.str.lower()

            data = []
            for values in list(df.to_dict(orient="records")):

                key = list(values)[1]
                value = values.get(key)

                chk_bot = BotsCrawJUD.query.filter_by(**{key: value}).first()

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

            return True

    except Exception as e:
        raise e
