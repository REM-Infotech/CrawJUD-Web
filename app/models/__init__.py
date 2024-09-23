from app import db
from app import app

from app.models.users import Users

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
                email="nicholas@robotz.dev")
            
            user.senhacrip = senha
            db.session.add(user)
            db.session.commit()
            
            print(f" * Root Pw: {senha}")
        
        