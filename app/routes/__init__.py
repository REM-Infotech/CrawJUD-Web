from flask import redirect, url_for, send_from_directory, make_response, abort
import os

def blueprint_reg(app):
    
    from app.routes.auth import auth
    from app.routes.dashboard import dash
    from app.routes.bot import bot
    from app.routes.execution import exe
    from app.routes.credentials import cred


    app.register_blueprint(auth)
    app.register_blueprint(dash)
    app.register_blueprint(bot)
    app.register_blueprint(exe)
    app.register_blueprint(cred)

    @app.route("/", methods = ["GET"])
    def index():
        
        return redirect(url_for("auth.login")), 302


    @app.route('/favicon.png', methods=["GET"])
    def serve_img():

        try:
            
            paht_icon = os.path.join(os.getcwd(), "static", "img")
            url = send_from_directory(paht_icon, "crawjud.png")
            return url

        except Exception as e:
            print(e)
            abort(500)