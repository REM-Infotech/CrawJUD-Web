from functools import wraps
from typing import Any
from flask import (
    current_app as app,
    flash,
    make_response,
    redirect,
    session,
    url_for,
    Response,
)
from flask_sqlalchemy import SQLAlchemy
from ..models import Users


def checkSu(func):
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | Any:

        usuario: str = session["login"]
        if query_supersu(usuario) is False:

            flash("Acesso negado", "error")
            return make_response(redirect(url_for("dash.dashboard")))

        return func(*args, **kwargs)

    return wrapper


def query_supersu(usuario: str) -> bool:

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    user = db.session.query(Users).filter(Users.login == usuario).first()

    if len(user.supersu) == 0:
        return False

    return True
