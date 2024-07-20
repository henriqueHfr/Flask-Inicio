from flask import render_template, url_for, request, redirect, flash, session, send_from_directory
from jogoteca import app, db
from middleware.login_required import login_required
from models.jogos import Jogos
from models.usuarios import Usuarios
from helpers.recupera_arquivo import recupera_imagem
from helpers.deleta_arquivo import deleta_arquivo
from helpers.FormularioJogo import FormularioJogo
import time

@app.route('/')
@login_required
def index():
    usuario = Usuarios.query.filter_by(id=session['usuario_logado']).first()
    if not usuario:
        return redirect(url_for('login'))
    lista = Jogos.query.filter_by(id_user=usuario.id).order_by(Jogos.id).all()
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioJogo()
    return render_template('novo.html', titulo='Novo Jogo', form=form)

@app.route('/criar', methods=['POST'])
def criar():
    form = FormularioJogo(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    if Jogos.query.filter_by(nome=nome).first():
        flash('Jogo já existente!')
        return redirect(url_for('index'))

    usuario = Usuarios.query.filter_by(id=session['usuario_logado']).first()
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console, id_user=usuario.id)
    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files.get('arquivo')
    if arquivo and arquivo.filename != '':
        timestamp = time.time()
        arquivo.save(f'{app.config["UPLOAD_PATH"]}/capa_{novo_jogo.id}_{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    jogo = Jogos.query.filter_by(id=id).first()
    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Jogo', form=form, id=id, capa_jogo=capa_jogo)

@app.route('/atualizar', methods=['POST'])
def atualizar():
    form = FormularioJogo(request.form)
    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data
        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files.get('arquivo')
        if arquivo and arquivo.filename != '':
            deleta_arquivo(jogo.id)
            timestamp = time.time()
            arquivo.save(f'{app.config["UPLOAD_PATH"]}/capa_{jogo.id}_{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash("O jogo foi deletado com sucesso")

    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory(app.config['UPLOAD_PATH'], nome_arquivo)





