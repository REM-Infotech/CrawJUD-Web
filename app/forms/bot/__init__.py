import os
import json
import pytz
import pathlib
from datetime import datetime

from flask_wtf import FlaskForm


from wtforms import (
    StringField, SubmitField, SelectField, SelectMultipleField, DateField)
from flask_wtf.file import FileField, FileAllowed, MultipleFileField

permited_file = FileAllowed(
    ['xlsx', 'xls', "csv"], 'Apenas arquivos |".xlsx"/".xls"/".csv"| são permitidos!')
permited_file2 = FileAllowed(
    ['pdf', 'jpg', "jpeg"], 'Apenas arquivos |".pdf"/".jpg"/".jpeg"| são permitidos!')


class BotForm(FlaskForm):

    xlsx = FileField("Arquivo do robô", validators=[
                     permited_file], render_kw={"accept": ".xlsx, .xls, .csv"})

    parte_name = StringField("Nome da parte")
    doc_parte = StringField("CPF/CNPJ da parte")
    polo_parte = SelectField("Classificação (Autor/Réu)", choices=[
        ("autor", "Autor"), ("reu", "Réu")])
    
    data_inicio = DateField(
        "Data de Início", default=datetime.now(pytz.timezone('Etc/GMT+4')))
    data_fim = DateField("Data Fim", default=datetime.now(
        pytz.timezone('Etc/GMT+4')))

    otherfiles = MultipleFileField(
        "Arquivo adicionais", validators=[permited_file2], render_kw={"accept": ".pdf, .jpg, .jpeg"})

    creds = SelectField("Selecione a Credencial", choices=[])
    password = StringField("Senha token")
    state = SelectField("Selecione o Estado", choices=[
                        ("Selecione", "Selecione")])
    varas = SelectMultipleField("Selecione a Vara", choices=[])
    client = SelectField("Selecione o Cliente", choices=[])
    submit = SubmitField("Iniciar Execução")

    def __init__(self, *args, dynamic_fields=None, **kwargs):
        super(BotForm, self).__init__(*args, **kwargs)

        # Remover os campos que não estão na lista de fields dinâmicos
        if dynamic_fields:
            # Remover campos que não estão na lista
            for field_name in list(self._fields.keys()):
                if field_name not in dynamic_fields:
                    del self._fields[field_name]

        if kwargs.get("system"):
            choices = []
            all_varas = varas().get(kwargs["system"].upper())
            if all_varas:
                for estado, juizados in all_varas.items():
                    for juizado, comarcas in juizados.items():
                        for comarca_key, comarca_value in comarcas.items():
                            choices.append((comarca_value, comarca_key, {
                                "data-juizado": f"{len(choices)}_{juizado}", "data-juizado_estado": f"{estado}"}))

        self.varas.choices.extend(choices)
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


def varas() -> dict[str, dict[str, dict[str, dict[str, str]]]]:

    file_p = pathlib.Path(__file__).parent.resolve()
    file_json = os.path.join(file_p, "varas.json")

    dict_files = {}

    with open(file_json, "rb") as f:
        obj = f.read()
        dict_files = json.loads(obj)

    return dict_files
