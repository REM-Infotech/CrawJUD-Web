from flask import Blueprint, render_template
from flask_login import login_required
import os
import pathlib

path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
bot = Blueprint("bot", __name__, template_folder=path_template)

from app.models import BotsCrawJUD

@bot.route("/bot/dashboard", methods = ["GET"])
@login_required
def dashboard():
    
    
    page = "botboard.html"
    bots = BotsCrawJUD.query.all()
    
    return render_template("index.html", page=page, bots=bots)   
