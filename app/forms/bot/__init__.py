from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed

permited_file = FileAllowed(['xlsx', 'xls',], 'Apenas arquivos ".xlsx" são permitidos!')

class BotForm(FlaskForm):
    
    xlsx = FileField("Arquivo do robô", validators=[FileRequired(), permited_file])
    submit = SubmitField("Entrar")
    
class CredentialsForm():
    
    creds = SelectField("Selecione a Credencial", choices=[("Selecione", "Selecione")])
    submit = SubmitField("Entrar")

