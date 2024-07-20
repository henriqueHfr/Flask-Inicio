from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField


class CriarUsuario(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=3, max=20)])
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=3, max=20)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=3, max=100)])
    cadastrar = SubmitField('Cadastrar')