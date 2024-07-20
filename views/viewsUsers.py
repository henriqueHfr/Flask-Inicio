from jogoteca import app, db
from flask import render_template, request, url_for, redirect, session, flash
from models.usuarios import Usuarios
from helpers.FormularioUsuario import FormularioUsuario
from helpers.CriarUsuario import CriarUsuario
from flask_bcrypt import check_password_hash
from flask_bcrypt import generate_password_hash

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormularioUsuario(request.form)

    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)
    if usuario and senha:
        session['usuario_logado'] = usuario.id
        flash(usuario.nickname + ' logado com sucesso!')
        return redirect('/')
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

@app.route('/cadastrar')
def cadastrar():
    form = CriarUsuario()
    return render_template('cadastro.html', form=form)

@app.route('/criar_usuario', methods=['POST',])
def criar_usuario():
    form = CriarUsuario(request.form)
    nome = form.nome.data
    nickname = form.nickname.data
    senha = generate_password_hash(form.senha.data).decode('utf-8')

    usuario = Usuarios.query.filter_by(nickname=nickname).first()
    if usuario:
        flash('Usuário ja cadastrado!')
        return redirect(url_for('cadastrar'))

    criar_novo_usuario = Usuarios(nome=nome, nickname=nickname, senha=senha)
    db.session.add(criar_novo_usuario)
    db.session.commit()
    return redirect(url_for('login'))