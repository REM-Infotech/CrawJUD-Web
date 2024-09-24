from app import login_manager
from flask import request
from flask_login import UserMixin
from uuid import uuid4
from datetime import datetime
import bcrypt
from app import db
import pytz
salt = bcrypt.gensalt()


@login_manager.user_loader
def load_user(user_id) -> int:

    link = request.referrer
    if link is None:
        link = request.url

    return Users.query.get(int(user_id))

licenses_users_bots = db.Table('licenses_users_bots',
    db.Column('licenses_user_id', db.Integer, db.ForeignKey('licenses_users.id'), primary_key=True),
    db.Column('bot_id', db.Integer, db.ForeignKey('bots.id'), primary_key=True)
)

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
    
    # Relacionamento com LicensesUsers
    licenses = db.relationship('LicensesUsers', backref='user', lazy=True)

    def __init__(self, login: str = None, nome_usuario: str = None,
                 email: str = None, license_key: str = None) -> None:

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
    id = db.Column(db.Integer, primary_key=True)
    name_client = db.Column(db.String(length=60), nullable=False, unique=True)
    cpf_cnpj = db.Column(db.String(length=30), nullable=False, unique=True)
    email_admin = db.Column(db.String(length=50), nullable=False, unique=True)
    license_token = db.Column(db.String(length=512), nullable=False, unique=True)
    
    # Foreign key para a tabela users
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Foreign key para a tabela Credentials
    credential_id = db.Column(db.Integer, db.ForeignKey('credentials.id'), nullable=False)
    
    # Relacionamento com Bots (conforme já definido antes)
    bots = db.relationship('BotsCrawJUD', secondary=licenses_users_bots, backref=db.backref('licenses_users', lazy=True))


