import os
from jogoteca import app
from helpers.recupera_arquivo import recupera_imagem

def deleta_arquivo(jogo_id):
    arquivo = recupera_imagem(jogo_id)
    if arquivo != 'capa_padrao.webp':
        arquivo_path = os.path.join(app.config['UPLOAD_PATH'], arquivo)
        if os.path.exists(arquivo_path):
            os.remove(arquivo_path)
        else:
            print(f"File not found: {arquivo_path}")
