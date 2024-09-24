from app.models import BotsCrawJUD
from flask import Blueprint, render_template, request, url_for
from flask_login import login_required
import os
import pathlib

path_template = os.path.join(pathlib.Path(
    __file__).parent.resolve(), "templates")
bot = Blueprint("bot", __name__, template_folder=path_template)


@bot.route("/bot/dashboard", methods=["GET"])
@login_required
def dashboard():

    page = "botboard.html"
    bots = BotsCrawJUD.query.all()

    return render_template("index.html", page=page, bots=bots)


@bot.route("/bot/<id>/<system>/<state>/<type>")
@login_required
def botlaunch(id: int, system: str, state: str, type: str):

    display_name = BotsCrawJUD.query.filter_by(id=id).first().display_name
    page = "botform.html"

    return render_template("index.html", page=page, url=request.base_url,
                           display_name=display_name)
