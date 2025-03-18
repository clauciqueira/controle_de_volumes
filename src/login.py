# -*- coding: utf-8 -*-
# login.py
import sys
import os  # Importa o módulo os para manipulação de caminhos
import time  # Importa o módulo time para pausar a execução do programa

# Adiciona o diretório raiz ao caminho de busca do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QLineEdit, QDesktopWidget
from Banco import database  # Importa o módulo database
from Doc import utils  # Importa o módulo utils
from main import MainWindow  # Importa a classe MainWindow


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
           
        # Garante que o caminho do arquivo UI esteja correto
        #uic.loadUi("ui/login.ui", self)  # Carrega a interface de login local

        ui_path = os.path.join(os.path.dirname(__file__), "ui", "login.ui")#carrgar para executar
        
        if not os.path.exists(ui_path): #verificar se o arquivo existe
            print(f"Erro: Arquivo {ui_path} não encontrado.") #exibir mensagem de erro
            sys.exit() #encerrar o programa
        uic.loadUi(ui_path, self) #carregar a interface de login local
    
        print(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "login.ui"))#carrgar para executar


        self.conexao = None  # Inicializa a conexão com o banco

        self.txt_usuario.textChanged.connect(self.validar_campos)
        self.txt_Senha.textChanged.connect(self.validar_campos)

        self.radioButtonVer.toggled.connect(self.mostrar_senha)
        self.btn_Login.clicked.connect(self.realizar_login)

        self.tentativas = 3  # Define o número de tentativas permitidas
        self.validar_campos()

        # Define o foco inicial no campo de usuário
        self.txt_usuario.setFocus()

        # Centraliza a tela de login
        self.centralizar_tela()

        self.show()

    def centralizar_tela(self):
        """
        Centraliza a tela de login na tela do usuário.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def inicializar_banco(self):
        """
        Inicializa a conexão com o banco de dados.
        """
        try:
            self.conexao = database.criar_conexao("localhost", "root", "1234", "controle_de_volumes")
            if self.conexao is None:
                utils.mostrar_mensagem("Erro",
                                        "Falha ao conectar ao banco de dados.  Verifique as configurações e tente novamente.",
                                        QMessageBox.Critical)
                sys.exit()
        except Exception as e:
            utils.mostrar_mensagem("Erro", f"Ocorreu um erro ao conectar ao banco de dados: {str(e)}",
                                    QMessageBox.Critical)
            sys.exit()

    def validar_campos(self):
        """
        Verifica se os campos de usuário e senha estão preenchidos para habilitar o botão de login.
        """
        usuario = self.txt_usuario.text().strip()
        senha = self.txt_Senha.text().strip()
        self.btn_Login.setEnabled(bool(usuario and senha))

    def mostrar_senha(self, checked):
        """
        Alterna a visibilidade da senha no campo de senha.
        """
        if checked: 
          self.txt_Senha.setEchoMode(QLineEdit.Normal)  # Mostra a senha
        else:
            self.txt_Senha.setEchoMode(QLineEdit.Password)  # Oculta a senha


    def realizar_login(self):
        """
        Realiza o processo de login, validando o usuário e a senha no banco de dados.
        """
        usuario = utils.converter_para_maiusculas(self.txt_usuario.text())
        senha = self.txt_Senha.text()

        if not usuario or not senha:
            utils.mostrar_mensagem("Erro", "Usuário e senha devem ser preenchidos.", QMessageBox.Warning)
            return

        # Inicializa a conexão com o banco de dados
        self.inicializar_banco()
        if not self.conexao:
            return  # Se a conexão falhar, interrompe o processo de login

        query = f"SELECT usuario, senha, tipo_usuario FROM usuarios WHERE usuario = '{usuario}'"
        resultado = database.executar_query_retorno(self.conexao, query)

        if resultado:
            usuario_db, senha_db, tipo_usuario = resultado[0]

        # Verifica se a senha fornecida corresponde ao hash armazenado  
        #if bcrypt.checkpw(senha.encode("utf-8"), senha_db.encode("utf-8")):  

            if senha == senha_db:
                utils.mostrar_mensagem("Sucesso", "Login realizado com sucesso!", QMessageBox.Information)
                self.abrir_main_window(usuario_db, tipo_usuario)
                self.close()
            else:
                self.tentativas -= 1
                utils.mostrar_mensagem("Erro", f"Senha incorreta. Tentativas restantes: {self.tentativas}",
                                        QMessageBox.Warning)
                if self.tentativas == 0:
                    utils.mostrar_mensagem("Erro", "Número de tentativas excedido. O programa será encerrado.",
                                            QMessageBox.Critical)
                    sys.exit()
        else:
            self.tentativas -= 1
            utils.mostrar_mensagem("Erro", f"Usuário não encontrado. Tentativas restantes: {self.tentativas}",
                                    QMessageBox.Warning)
            if self.tentativas == 0:
                utils.mostrar_mensagem("Erro", "Número de tentativas excedido. O programa será encerrado.",
                                        QMessageBox.Critical)
                sys.exit()
        if self.conexao: #Se existir
            database.fechar_conexao(self.conexao)  # fecha conexão

    def abrir_main_window(self, usuario, tipo_usuario):
        """
        Abre a janela principal (MainWindow) após o login bem-sucedido.
        """
        #self.main_window = MainWindow(usuario, tipo_usuario)
        #self.main_window.show()
        
        try:  
            self.main_window = MainWindow(usuario,tipo_usuario)  
            self.main_window.show()  
        except Exception as e:  
            print(f"Erro ao criar ou exibir a tela principal: {e}") 






    def closeEvent(self, event):
        """
        Evento executado ao fechar a janela de login.
        Garante que a conexão com o banco seja fechada.
        """
        if self.conexao:
            database.fechar_conexao(self.conexao)
        event.accept()  # Aceita o fechamento da janela


if __name__ == '__main__':
    app = QApplication(sys.argv)  # Cria a instância de QApplication *ANTES* de qualquer widget
    login = Login()
    sys.exit(app.exec_())