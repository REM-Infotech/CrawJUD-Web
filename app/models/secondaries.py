from app import db


admins = db.Table(
    'admins', 
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('license_user_id', db.Integer, db.ForeignKey('licenses_users.id'), primary_key=True))


execution_bots = db.Table(
    'execution_bots',
    db.Column('bot_id', db.Integer, db.ForeignKey('bots.id'), primary_key=True),
    db.Column('licenses_users_id', db.Integer, db.ForeignKey('licenses_users.id'), primary_key=True))
