# -*- coding: utf-8 -*-
import re
from PyQt5.QtWidgets import QMessageBox

def validar_telefone(telefone):
    """
    Valida um número de telefone usando uma expressão regular.

    Args:
        telefone (str): O número de telefone a ser validado.

    Returns:
        bool: True se o telefone for válido, False caso contrário.
    """
    padrao = re.compile(r"^\(\d{2}\) \d{4,5}-\d{4}$")  # Ex: (54) 99999-9999 ou (54) 9999-9999
    return bool(padrao.match(telefone))

def mostrar_mensagem(titulo, mensagem, icone=QMessageBox.Information):
    """
    Exibe uma caixa de mensagem ( QMessageBox ) com o título, mensagem e ícone especificados.

    Args:
        titulo (str): O título da caixa de mensagem.
        mensagem (str): A mensagem a ser exibida na caixa de mensagem.
        icone (QMessageBox.Icon): O ícone a ser exibido na caixa de mensagem.  Pode ser:
            QMessageBox.Information (padrão)
            QMessageBox.Warning
            QMessageBox.Critical
            QMessageBox.Question
    """
    msg_box = QMessageBox()
    msg_box.setWindowTitle(titulo)
    msg_box.setText(mensagem)
    msg_box.setIcon(icone)
    msg_box.exec_()

def limpar_campos(widgets):
    """
    Limpa o texto de uma lista de widgets (QLineEdit, QPlainTextEdit, etc.).

    Args:
        widgets (list): Uma lista de widgets a serem limpos.
    """
    for widget in widgets:
        if hasattr(widget, 'clear'):
            widget.clear()
        elif hasattr(widget, 'setValue'):  # Para QSpinBox
            widget.setValue(0)  # Define o valor padrão como 0 (ou outro valor apropriado)
        elif hasattr(widget, 'setChecked'): # Para QCheckBox
            widget.setChecked(False) # Desmarca a checkbox

def converter_para_maiusculas(texto):
    """
    Converte um texto para maiúsculas e remove espaços em branco extras.

    Args:
        texto (str): O texto a ser convertido.

    Returns:
        str: O texto convertido para maiúsculas, sem espaços em branco extras.
    """
    if texto:
        return texto.upper().strip()
    return ""  # Retorna uma string vazia se o texto for None ou vazio