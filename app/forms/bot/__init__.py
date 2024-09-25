from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, SubmitField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed

permited_file = FileAllowed(['xlsx', 'xls', ".csv"], 'Apenas arquivos ".xlsx"|".xls"|".csv" são permitidos!')

class BotForm(FlaskForm):
    
    xlsx = FileField("Arquivo do robô", validators=[FileRequired(), permited_file], render_kw={"accept": ".xlsx, .xls, .csv"})
    creds = SelectField("Selecione a Credencial", choices=[("Selecione", "Selecione")])
    state = SelectField("Selecione o Estado", choices=[("Selecione", "Selecione")])
    submit = SubmitField("Iniciar Execução")
    
    def __init__(self, *args, **kwargs):
        super(BotForm, self).__init__(*args, **kwargs)
        
        states = kwargs.get("state")
        if states:
            self.state.choices.extend(states)
