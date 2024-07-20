from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators,PasswordField



class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname',[validators.DataRequired(), validators.length(min=1, max=20)])
    senha = PasswordField('Senha',[validators.DataRequired(), validators.length(min=2, max=100)])
    login = SubmitField('Login')