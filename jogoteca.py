from flask import Flask, render_template, request, redirect, session, flash, url_for

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

lista = []
app = Flask(__name__)
app.secret_key = 'alura'

class Usuarios:
    def __init__(self, nome, usuario, senha):
        self.nome = nome
        self.nickname = usuario
        self.senha = senha


usuario1 = Usuarios('Henrique', 'Racknarok', '260105')
usuario2 = Usuarios('Grazy', 'gryzinha', '240207')
usuario3 = Usuarios('Sergio', 'Nascims', '050372')

usuarios = {usuario1.nickname: usuario1, usuario2.nickname: usuario2, usuario3.nickname: usuario3}

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo')

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + 'Usuário logado com sucesso')
            proxima_route = request.form.get('proxima', url_for('index'))
            return redirect(proxima_route)
    else:
        flash('Usuário não logado')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('index'))

app.run(debug=True)
