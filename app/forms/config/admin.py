from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class UserForm(FlaskForm):

    nome_usuario = StringField(label="Nome", validators=[DataRequired()])
    login = StringField(label="Login", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(
        label="Senha", validators=[DataRequired(), Length(min=8, max=62)]
    )
    show_password = BooleanField("Exibir senha", id="check")
    tipo_user = SelectField(
        label="Tipo de usuário",
        choices=[("default_user", "Usuário Padrão"), ("admin", "Administrador")],
    )

    licenses = SelectField(label="Selecione a Licença", choices=[])
    submit = SubmitField(label="Salvar Alterações")

    def __init__(
        self, tipoUsr: str = None, licenses: list[tuple] = None, *args, **kwargs
    ):

        super().__init__(*args, **kwargs)
        if tipoUsr:

            self.tipo_user.choices.extend([tipoUsr])
            self.licenses.choices.extend(licenses)

        elif tipoUsr is None:
            del self.licenses
