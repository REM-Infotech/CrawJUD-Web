from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SubmitField

from app.forms.auth.login import LoginForm
from app.forms.bot import BotForm, SearchExec
from app.forms.config import UserForm
from app.forms.credentials import CredentialsForm

__all__ = [LoginForm, BotForm, SearchExec, CredentialsForm, UserForm]


permited_file = FileAllowed(["xlsx", "xls"], 'Apenas arquivos ".xlsx" são permitidos!')


class IMPORTForm(FlaskForm):

    arquivo = FileField(
        label="Arquivo de importação. Máximo 50Mb",
        validators=[FileRequired(), permited_file],
    )
    submit = SubmitField(label="Importar")
