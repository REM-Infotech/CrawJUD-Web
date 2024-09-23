from flask import Blueprint, render_template

import os
import pathlib

path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")

auth = Blueprint("auth", __name__, template_folder=path_template)

@auth.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    return ""

@auth.route("/logout", methods=["GET", "POST"])
def logout():
    return ""

