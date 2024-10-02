from flask import Blueprint, render_template
from flask_login import login_required

import os
import pathlib

path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
exe = Blueprint("exe", __name__, template_folder=path_template)

@exe.route("/executions", methods = ["GET"])
@login_required
def executions():
    
    title = "Execuções"
    page = "executions.html"
    return render_template("index.html", page=page, title=title)   
