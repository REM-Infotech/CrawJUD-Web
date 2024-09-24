from app import db

class BaseTextBots(db.Model):
    
    __tablename__ = 'TextBots'
    id = db.Column(db.Integer, primary_key=True)
    bot_name = db.Column(db.String(length=45), nullable=False)
    TitleBot = db.Column(db.String(length=45), nullable=False)
    TextBots = db.Column(db.String(length=512), nullable=False)
