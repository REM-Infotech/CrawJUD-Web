from flask import Blueprint, render_template

import os
import pathlib

path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
dash = Blueprint("dash", __name__, template_folder=path_template)

@dash.route("/dashboard", methods = ["GET"])
def dashboard():
    
    page="dashboard.html"
    return render_template("index.html", page=page)   