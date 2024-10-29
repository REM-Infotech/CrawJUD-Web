from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class UserForm(FlaskForm):
    
    nome = StringField(label="Nome", validators=[DataRequired()])
    login = StringField(label="Login", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Senha", validators=[DataRequired(), Length(min=8, max=62)])
    show_password = BooleanField('Exibir senha', id='check')
    tipo_user = SelectField(label="Tipo de usuário", choices=[("default_user", "Usuário Padrão")])
    submit = SubmitField(label="Salvar Alterações")
    
    def __init__(self, *args, **kwargs):
        
        
        super().__init__(*args, **kwargs)
