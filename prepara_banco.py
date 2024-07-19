import mysql.connector
from mysql.connector import errorcode

try:
    print("Conectando...")
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='admin'
    )

    cursor = conn.cursor()

    cursor.execute("DROP DATABASE IF EXISTS `jogoteca`;")
    cursor.execute("CREATE DATABASE `jogoteca`;")
    cursor.execute("USE `jogoteca`;")

    # Criando tabelas
    TABLES = {}
    TABLES['Jogos'] = '''
        CREATE TABLE `jogos` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `nome` varchar(50) NOT NULL,
        `categoria` varchar(40) NOT NULL,
        `console` varchar(20) NOT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    '''

    TABLES['Usuarios'] = '''
        CREATE TABLE `usuarios` (
        `nome` varchar(20) NOT NULL,
        `nickname` varchar(20) NOT NULL,
        `senha` varchar(100) NOT NULL,
        PRIMARY KEY (`nickname`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    '''

    for tabela_nome in TABLES:
        tabela_sql = TABLES[tabela_nome]
        try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
            print('OK')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print('Já existe')
            else:
                print(err.msg)

    # Inserindo usuários
    usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
    usuarios = [
        ("Henrique", "Racknarok", "260105"),
        ("Grazy", "grzynha", "240207"),
        ("Sergio", "Nascims", "Spfc5181")
    ]
    cursor.executemany(usuario_sql, usuarios)

    # Exibindo usuários inseridos
    cursor.execute('SELECT * FROM usuarios')
    print(' -------------  Usuários:  -------------')
    for user in cursor.fetchall():
        print(user[1])

    # Inserindo jogos
    jogos_sql = 'INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s)'
    jogos = [
        ('Tetris', 'Puzzle', 'Atari'),
        ('God of War', 'Hack n Slash', 'PS2'),
        ('Mortal Kombat', 'Luta', 'PS2'),
        ('Valorant', 'FPS', 'PC'),
        ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
        ('Need for Speed', 'Corrida', 'PS2'),
    ]
    cursor.executemany(jogos_sql, jogos)

    # Exibindo jogos inseridos
    cursor.execute('SELECT * FROM jogos')
    print(' -------------  Jogos:  -------------')
    for jogo in cursor.fetchall():
        print(jogo[1])

    # Commitando as operações no banco
    conn.commit()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print('O banco de dados não existe')
    else:
        print(err)

except Exception as e:
    print(f"Ocorreu um erro: {e}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
