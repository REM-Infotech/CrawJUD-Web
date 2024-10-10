from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, SubmitField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed, MultipleFileField

permited_file = FileAllowed(['xlsx', 'xls', "csv"], 'Apenas arquivos |".xlsx"/".xls"/".csv"| são permitidos!')
permited_file2 = FileAllowed(['pdf', 'jpg', "jpeg"], 'Apenas arquivos |".pdf"/".jpg"/".jpeg"| são permitidos!')


class BotForm(FlaskForm):
    
    xlsx = FileField("Arquivo do robô", validators=[FileRequired(), permited_file], render_kw={"accept": ".xlsx, .xls, .csv"})
    otherfiles = MultipleFileField("Arquivo adicionais", validators=[permited_file2], render_kw={"accept": ".pdf, .jpg, .jpeg"})
    creds = SelectField("Selecione a Credencial", choices=[("Selecione", "Selecione")])
    password = StringField("Senha token")
    state = SelectField("Selecione o Estado", choices=[("Selecione", "Selecione")])
    client = SelectField("Selecione o Cliente", choices=[("Selecione", "Selecione")])
    submit = SubmitField("Iniciar Execução")
    
    def __init__(self, *args, dynamic_fields=None, **kwargs):
        super(BotForm, self).__init__(*args, **kwargs)
        
        # Remover os campos que não estão na lista de fields dinâmicos
        if dynamic_fields:
            # Remover campos que não estão na lista
            for field_name in list(self._fields.keys()):
                if field_name not in dynamic_fields:
                    del self._fields[field_name]

        # Se tiver 'state' e 'creds' no kwargs, popular as escolhas
        if kwargs.get("state"):
            self.state.choices.extend(kwargs.get("state"))
            
        if kwargs.get("clients"):
            self.client.choices.extend(kwargs.get("clients"))   
        
        if kwargs.get("creds"):
            self.creds.choices.extend(kwargs.get("creds"))

class SearchExec(FlaskForm):
    
    campo_busca = StringField("Buscar Execução")
    submit = SubmitField("Buscar")
