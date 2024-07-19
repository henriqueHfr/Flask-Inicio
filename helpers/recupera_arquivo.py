import os
from jogoteca import app
def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa_{id}' in nome_arquivo:
            print(nome_arquivo)
            return nome_arquivo
    return 'capa-padrao.webp'