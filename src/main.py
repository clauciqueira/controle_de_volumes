# -*- coding: utf-8 -*-
# main.py
import locale
from datetime import datetime, date
from tab_loja import LojaApp
from tab_usuario import TabUsuario
from TabRelatorio import TabRelatorio
from tab_volumes import TabVolumes
from tab_feira import TabFeira  # Importa a classe TabFeira
from Doc import utils
from Banco import database
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QWidget, QTabWidget, QPushButton, QStackedWidget, QDesktopWidget
from PyQt5 import uic
import sys
import os
import traceback

# Adiciona o diretório pai do diretório atual ao caminho de busca de módulos do Python.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define o locale para português do Brasil para formatação de números e datas.
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class MainWindow(QMainWindow):
    """
    Classe que representa a janela principal da aplicação.
    """

    def __init__(self, usuario, tipo_usuario):
        """
        Inicializa a janela principal.

        Args:
            usuario (str): O nome do usuário logado.
            tipo_usuario (str): O tipo de usuário (ex: 'administrador', 'comum').
        """


class MainWindow(QMainWindow):  # Garanta que herda de QMainWindow  
    def __init__(self, usuario, tipo_usuario):  
        super().__init__()  # Chama o construtor da classe pai  
        # Garante que o caminho do arquivo UI esteja correto  
        #uic.loadUi("ui/main.ui", self)  # Carrega a interface gráfica local

        ui_path = os.path.join(os.path.dirname(__file__), "ui", "main.ui")  # Ajuste o nome do arquivo, se necessário  
        if not os.path.exists(ui_path):  
            print(f"Erro: Arquivo {ui_path} não encontrado.")  
            sys.exit()  

        uic.loadUi(ui_path, self)  


        self.usuario = usuario
        self.tipo_usuario = tipo_usuario
        self.conexao = None

        # Inicializa o Stacked Widget
        try:
            self.stackedWidget = self.findChild( QStackedWidget, "stackedWidget")
            self.page = self.findChild(QWidget, "page")
            self.page_2 = self.findChild(QWidget, "page_2")
            self.stackedWidget.setCurrentWidget( self.page)  # Define a página inicial
            print("StackedWidget inicializado")
        except Exception as e:
            print(f"Erro ao inicializar o StackedWidget: {e}")

        # Conexão com o banco de dados
        self.inicializar_banco()

        # Inicializa as abas
        try:
            self.tab_volume = self.findChild(QWidget, "tab_volume")
            self.tab_relatorio = self.findChild(QWidget, "tab_relatorio")
            self.tab_loja = self.findChild(QWidget, "tab_loja")
            self.tab_usuario = self.findChild(QWidget, "tab_usuario")
            self.tab_feira = self.findChild(QWidget, "tab_feira")
            self.tabWidget = self.findChild(QTabWidget, "tabWidget")
            print("Abas inicializadas")
        except Exception as e:
            print(f"Erro ao inicializar as abas: {e}")

        # Inicializa os botões
        try:
            self.btn_volumes = self.findChild(QPushButton, "btn_volumes")
            self.btn_Relatorio = self.findChild(QPushButton, "btn_Relatorio")
            self.btn_loja = self.findChild(QPushButton, "btn_loja")
            self.btn_Usuario = self.findChild(QPushButton, "btn_Usuario")
            self.btn_feiras = self.findChild(QPushButton, "btn_feiras")
            self.btn_Sair = self.findChild(QPushButton, "btn_Sair")
            print("Botões inicializados")
        except Exception as e:
            print(f"Erro ao inicializar os botões: {e}")

        # Oculta o botão Feiras se o tipo de usuário for "usuario"
        if tipo_usuario == "usuario" and self.btn_feiras:
            self.btn_feiras.setVisible(False)
            print("Botão Feiras ocultado para usuário comum")

        # Inicializa os widgets das abas
        self.inicializar_abas()

        # Ajusta a visibilidade das abas e botões com base no tipo de usuário.
        self.configurar_interface(tipo_usuario)

        # Centraliza a tela principal
        self.centralizar_tela()
        #self.showFullScreen()  # Abre em tela cheia  
    

        # Conectar botões às funções
        self.conectar_botoes()

        # Exibe a janela principal.
        #self.show()
        print("Janela principal exibida")

    def centralizar_tela(self):
        """
        Centraliza a tela principal na tela do usuário.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def inicializar_banco(self):
        """
        Inicializa a conexão com o banco de dados.
        """
        print("Inicializando conexão com o banco de dados")
        try:
            self.conexao = database.criar_conexao(
                "localhost", "root", "1234", "controle_de_volumes")
            if self.conexao is None:
                utils.mostrar_mensagem("Erro",
                                       "Falha ao conectar ao banco de dados. Verifique as configurações e tente novamente.",
                                       QMessageBox.Critical)
                sys.exit()
            print("Conexão com o banco de dados estabelecida")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            utils.mostrar_mensagem("Erro", f"Ocorreu um erro ao conectar ao banco de dados: {str(e)}",
                                   QMessageBox.Critical)
            sys.exit()

    def inicializar_abas(self):
        """
        Inicializa os widgets das abas e conecta os sinais aos slots.
        """
        print("Inicializando widgets das abas")
        try:
            self.tab_volumes_widget = TabVolumes(  self.conexao, self.tab_volume, self, self.usuario)
            self.tab_relatorio_widget = TabRelatorio(  self.conexao, self.tab_relatorio)
            self.tab_usuario_widget = TabUsuario( self.conexao, self.tab_usuario, self, self.usuario)
            self.tab_loja_widget = LojaApp(   self.conexao, self.tab_loja, self, self.usuario)
            self.tab_feira_widget = TabFeira(  self.conexao, self.tab_feira, self, self.usuario)
            print("Widgets das abas inicializados")
        except Exception as e:
            print(f"Erro ao inicializar os widgets das abas: {e}")

    def conectar_botoes(self):
        """
        Conecta os botões às funções apropriadas.
        """
        try:
            self.btn_volumes.clicked.connect(self.abrir_aba_volumes)
            self.btn_Relatorio.clicked.connect(self.abrir_aba_relatorio)
            self.btn_loja.clicked.connect(self.abrir_aba_loja)
            self.btn_Usuario.clicked.connect(self.abrir_aba_usuario)
            if self.btn_feiras and self.tab_feira:
                print("Conectando btn_feiras ao slot")
                self.btn_feiras.clicked.connect(self.abrir_aba_feira)
            self.btn_Sair.clicked.connect(self.logout)
            print("Sinais conectados aos botões")
        except Exception as e:
            print(f"Erro ao conectar sinais aos botões: {e}")

    def configurar_interface(self, tipo_usuario):
        """
        Configura a interface com base no tipo de usuário.
        """
        print(f"Configurando interface para o tipo de usuário: {tipo_usuario}")
        try:
            if tipo_usuario == "administrador":
                self.btn_volumes.setVisible(True)
                self.btn_Relatorio.setVisible(True)
                self.btn_loja.setVisible(True)
                self.btn_Usuario.setVisible(True)
                if self.btn_feiras:
                    self.btn_feiras.setVisible(True)
                self.tabWidget.setTabVisible(0, True)  # Volumes
                self.tabWidget.setTabVisible(1, True)  # Relatório
                self.tabWidget.setTabVisible(2, True)  # Loja
                self.tabWidget.setTabVisible(3, True)  # Usuários
                self.tabWidget.setTabVisible(4, True)  # Feira
            elif tipo_usuario == "usuario":
                self.btn_volumes.setVisible(True)
                self.btn_Relatorio.setVisible(True)
                self.btn_loja.setVisible(False)
                self.btn_Usuario.setVisible(False)
                if self.btn_feiras:
                    self.btn_feiras.setVisible(False)
                self.tabWidget.setTabVisible(0, True)  # Volumes
                self.tabWidget.setTabVisible(1, True)  # Relatório
                self.tabWidget.setTabVisible(2, False)  # Oculta Loja
                self.tabWidget.setTabVisible(3, False)  # Oculta Usuários
                self.tabWidget.setTabVisible(4, False)  # Oculta Feira
            print("Interface configurada")
        except Exception as e:
            print(f"Erro ao configurar a interface: {e}")

    def logout(self):
        """
        Realiza o logout do usuário, fechando a conexão com o banco de dados e retornando à tela de login.
        """
        print("Realizando logout")
        try:
            if self.conexao:
                database.fechar_conexao(self.conexao)
            self.stackedWidget.setCurrentWidget(self.page)
            self.close()
            print("Logout realizado")
        except Exception as e:
            print(f"Erro ao realizar logout: {e}")

    def closeEvent(self, event):
        """
        Sobrescreve o método closeEvent para garantir que a conexão com o banco de dados seja fechada antes de fechar a janela.
        """
        print("Fechando janela principal")
        try:
            if self.conexao:
                database.fechar_conexao(self.conexao)
            event.accept()
            print("Janela principal fechada")
        except Exception as e:
            print(f"Erro ao fechar a janela principal: {e}")

    def abrir_aba_volumes(self):
        """
        Abre a aba de volumes.
        """
        self.stackedWidget.setCurrentWidget(self.page_2)
        self.tabWidget.setCurrentWidget(self.tab_volume)

    def abrir_aba_relatorio(self):
        """
        Abre a aba de relatório e carrega os dados.
        """
        self.stackedWidget.setCurrentWidget(self.page_2)
        self.tabWidget.setCurrentWidget(self.tab_relatorio)
        self.tab_relatorio_widget.carregar_dados()

    def abrir_aba_loja(self):
        """
        Abre a aba de loja.
        """
        self.stackedWidget.setCurrentWidget(self.page_2)
        self.tabWidget.setCurrentWidget(self.tab_loja)

    def abrir_aba_usuario(self):
        """
        Abre a aba de usuário.
        """
        self.stackedWidget.setCurrentWidget(self.page_2)
        self.tabWidget.setCurrentWidget(self.tab_usuario)

    def abrir_aba_feira(self):
        """
        Abre a aba de feira.
        """
        self.stackedWidget.setCurrentWidget(self.page_2)
        self.tabWidget.setCurrentWidget(self.tab_feira)


def get_caminho_relativo(caminho):
    """Retorna o caminho correto dentro do executável ou do ambiente normal"""
    if getattr(sys, 'frozen', False):  # Se estiver rodando como .exe
        return os.path.join(sys._MEIPASS, caminho)
    return caminho

def main():
    try:
        # Código principal do programa
        print("Iniciando aplicação...")
        # Simulando erro para debug
        # raise Exception("Erro de teste!")
    except Exception as e:
        erro = traceback.format_exc()
        with open("erro_log.txt", "w") as log:
            log.write(erro)
        print("Ocorreu um erro! Veja erro_log.txt para mais detalhes.")


if __name__ == '__main__':
    try:
        print("Iniciando aplicação")
        app = QApplication(sys.argv)
        # Alterado para "usuario" para teste
        window = MainWindow("usuario_teste", "usuario")
        sys.exit(app.exec_())
        print("Aplicação encerrada")
    except Exception as e:
        # Captura e exibe o erro no console
        print("Um erro ocorreu:")
        traceback.print_exc()  # Exibe o rastreamento do erro
        input("Pressione Enter para fechar...")  # Aguarda o usuário pressionar Enter

