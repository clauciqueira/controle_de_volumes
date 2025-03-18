import sys
import os

def get_caminho_relativo(caminho):
    """ Retorna o caminho correto dentro do executável ou do ambiente normal """
    if getattr(sys, 'frozen', False):  # Se estiver rodando como .exe
        return os.path.join(sys._MEIPASS, caminho)
    return caminho  # Se estiver rodando normalmente

caminho_arquivo = get_caminho_relativo("ui/main.ui")