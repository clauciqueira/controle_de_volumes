import sys
import os
import bcrypt  # Biblioteca para hashing de senhas
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QApplication, QLineEdit, QPushButton, QRadioButton, QTableWidget
import mysql.connector
from Banco import database  # Importa a conexão com o banco

# Ajusta o caminho do projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TabUsuario(QWidget):
    def __init__(self, conexao, tab_usuario_widget, main_window, usuario):
        super(TabUsuario, self).__init__()
        self.conexao = conexao  # Conexão com MySQL
        self.tab_usuario = tab_usuario_widget  # Referência à aba
        self.main_window = main_window  # Referência à janela principal
        self.usuario = usuario  # Usuário logado

        # Inicializa os widgets
        self.txt_CadastroUsuario = self.tab_usuario.findChild(
            QLineEdit, "txt_CadastroUsuario")
        self.txt_CadastroSenha = self.tab_usuario.findChild(
            QLineEdit, "txt_CadastroSenha")
        self.txt_CadastroSenhaConfirma = self.tab_usuario.findChild(
            QLineEdit, "txt_CadastroSenhaConfirma")
        self.radioButtonAdm = self.tab_usuario.findChild(
            QRadioButton, "radioButtonAdm")
        self.radioButtonUser = self.tab_usuario.findChild(
            QRadioButton, "radioButtonUser")
        self.btn_InserirUsuario = self.tab_usuario.findChild(
            QPushButton, "btn_InserirUsuario")
        self.btn_ApagarUsuario = self.tab_usuario.findChild(
            QPushButton, "btn_ApagarUsuario")
        self.tableWidgetUsuario = self.tab_usuario.findChild(
            QTableWidget, "tableWidgetUsuario")

        # Conecta os botões às funções
        self.btn_InserirUsuario.clicked.connect(self.inserir_usuario)
        self.btn_ApagarUsuario.clicked.connect(self.apagar_usuario)

        # Atualiza a tabela ao iniciar
        self.atualizar_tabela()

    def inserir_usuario(self):
        """Insere um novo usuário no banco de dados"""
        usuario = self.txt_CadastroUsuario.text().strip().upper()
        senha = self.txt_CadastroSenha.text().strip()
        senha_confirma = self.txt_CadastroSenhaConfirma.text().strip()
        tipo_usuario = "administrador" if self.radioButtonAdm.isChecked() else "usuario"

        # Verifica se os campos foram preenchidos
        if not usuario or not senha or not senha_confirma:
            QMessageBox.warning(
                self, "Erro", "Todos os campos devem ser preenchidos!")
            return

        # Verifica se as senhas coincidem
        if senha != senha_confirma:
            QMessageBox.warning(self, "Erro", "As senhas não conferem!")
            return

        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
            if cursor.fetchone():
                QMessageBox.warning(self, "Erro", "Usuário já existe!")
                return

            # Gera um hash seguro para a senha
#            senha_hash = bcrypt.hashpw(senha.encode(
 #               "utf-8"), bcrypt.gensalt()).decode("utf-8")

            cursor.execute("INSERT INTO usuarios (usuario, senha, tipo_usuario) VALUES (%s, %s, %s)",
                           (usuario, senha, tipo_usuario))
            self.conexao.commit()
            cursor.close()

            QMessageBox.information(
                self, "Sucesso", "Usuário cadastrado com sucesso!")
            self.atualizar_tabela()
            self.limpar_campos()
        except mysql.connector.Error as e:
            QMessageBox.critical(
                self, "Erro", f"Erro ao inserir usuário: {str(e)}")

    def apagar_usuario(self):
        """Apaga um usuário selecionado na tabela"""
        linha_selecionada = self.tableWidgetUsuario.currentRow()
        if linha_selecionada == -1:
            QMessageBox.warning(
                self, "Erro", "Selecione um usuário para excluir!")
            return

        usuario = self.tableWidgetUsuario.item(linha_selecionada, 0).text()

        resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja excluir o usuário '{usuario}'?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resposta == QMessageBox.No:
            return

        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "DELETE FROM usuarios WHERE usuario = %s", (usuario,))
            self.conexao.commit()
            cursor.close()

            QMessageBox.information(
                self, "Sucesso", "Usuário excluído com sucesso!")
            self.atualizar_tabela()
        except mysql.connector.Error as e:
            QMessageBox.critical(
                self, "Erro", f"Erro ao excluir usuário: {str(e)}")

    def atualizar_tabela(self):
        """Atualiza a tabela de usuários"""
        try:
            cursor = self.conexao.cursor()
            cursor.execute("SELECT usuario, tipo_usuario FROM usuarios")
            usuarios = cursor.fetchall()
            cursor.close()

            self.tableWidgetUsuario.setRowCount(len(usuarios))
            self.tableWidgetUsuario.setColumnCount(2)
            self.tableWidgetUsuario.setHorizontalHeaderLabels(
                ["Usuário", "Tipo"])

            for i, (usuario, tipo) in enumerate(usuarios):
                self.tableWidgetUsuario.setItem(
                    i, 0, QTableWidgetItem(usuario))
                self.tableWidgetUsuario.setItem(i, 1, QTableWidgetItem(tipo))
        except mysql.connector.Error as e:
            QMessageBox.critical(
                self, "Erro", f"Erro ao atualizar tabela: {str(e)}")

    def limpar_campos(self):
        """Limpa os campos de entrada"""
        self.txt_CadastroUsuario.clear()
        self.txt_CadastroSenha.clear()
        self.txt_CadastroSenhaConfirma.clear()
        self.radioButtonAdm.setChecked(False)
        self.radioButtonUser.setChecked(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    conexao = database.connect()  # Substitua pelo objeto de conexão real
    tab_usuario_widget = None  # Substitua pelo widget real
    main_window = None  # Substitua pela janela principal real
    usuario = None  # Substitua pelo usuário real
    window = TabUsuario(conexao, tab_usuario_widget, main_window, usuario)
    window.show()
    sys.exit(app.exec_())
