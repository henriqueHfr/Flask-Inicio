from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField


class FormularioJogo(FlaskForm):
    nome = StringField('Nome do Jogo', [validators.DataRequired(), validators.Length(min=3, max=50)])
    categoria = StringField('Categoria', [validators.DataRequired(), validators.Length(min=3, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')