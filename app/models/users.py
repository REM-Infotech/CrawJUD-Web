from flask import request
from flask_login import UserMixin

from app import db
from app import login_manager

import pytz
from uuid import uuid4
from typing import Type
from datetime import datetime
import bcrypt


from sqlalchemy.orm.relationships import RelationshipProperty
salt = bcrypt.gensalt()


@login_manager.user_loader
def load_user(user_id) -> int:

    link = request.referrer
    if link is None:
        link = request.url

    return Users.query.get(int(user_id))

class SuperUser(db.Model):
    
    __tablename__ = "superuser"
    id: int = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('Users', backref=db.backref('supersu', lazy=True))

class Users(db.Model, UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(length=30), nullable=False, unique=True)
    nome_usuario = db.Column(db.String(length=64), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Etc/GMT+4')))
    verification_code = db.Column(db.String(length=45), unique=True)
    login_id = db.Column(db.String(length=64), nullable=False, default=str(uuid4()))
    filename = db.Column(db.String(length=128))
    blob_doc = db.Column(db.LargeBinary(length=(2**32)-1))
    executions = db.relationship('Executions', secondary="execution_users",
                                 backref=db.backref('executions', lazy=True))
    
    def __init__(self, login: str = None, nome_usuario: str = None,
                 email: str = None) -> None:

        self.login = login
        self.nome_usuario = nome_usuario
        self.email = email

    @property
    def senhacrip(self):
        return self.senhacrip

    @senhacrip.setter
    def senhacrip(self, senha_texto: str):
        self.password = bcrypt.hashpw(
            senha_texto.encode(), salt).decode("utf-8")

    def check_password(self, senha_texto_claro: str) -> bool:
        return bcrypt.checkpw(senha_texto_claro.encode("utf-8"), self.password.encode("utf-8"))

class LicensesUsers(db.Model):
    
    __tablename__ = 'licenses_users'
    id: int = db.Column(db.Integer, primary_key=True)
    name_client: str = db.Column(db.String(length=60), nullable=False, unique=True)
    cpf_cnpj: str = db.Column(db.String(length=30), nullable=False, unique=True)
    license_token: str = db.Column(db.String(length=512), nullable=False, unique=True)
    
    # Relacionamento de muitos para muitos com users
    users = db.relationship('Users', secondary="licenseusr", backref='licenses')
    admins = db.relationship('Users', secondary="admins", backref='admin')
    
    # Relacionamento de muitos para muitos com Credentials
    credentials = db.relationship('Credentials', secondary="licenses_users_credentials", 
                                  backref=db.backref('license', lazy=True))
    
    executions = db.relationship('Executions', secondary='execution_licenses', 
                                 backref=db.backref('license', lazy=True))
    
    bots = db.relationship('BotsCrawJUD', secondary="licenses_users_bots", 
                           backref=db.backref('license', lazy=True))
