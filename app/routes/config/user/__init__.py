from flask import Blueprint, render_template
from flask_login import login_required
import os
import pathlib

path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
usr = Blueprint("usr", __name__, template_folder=path_template)


@usr.route("/profile_config", methods=["GET", "POST"])
@login_required
def profile_config():

    pagina = "config_page.html"
    return render_template("index.html", pagina=pagina)
