import sys  # Importa o módulo sys para manipulação do sistema
import os  # Importa o módulo os para manipulação do sistema operacional
import logging  # Importa o módulo logging para registro de logs
from PyQt5 import uic  # Importa o módulo uic do PyQt5 para carregar arquivos .ui
import locale  # Importa o módulo locale para manipulação de localizações
from Banco import database  # Importa o módulo database do pacote Banco
from Doc import utils  # Importa o módulo utils do pacote Doc
from PyQt5.QtWidgets import QWidget, QMessageBox, QTreeWidgetItem, QLineEdit, QPushButton, QTreeWidget, QDateEdit, QTableWidgetItem, QTableWidget, QApplication  # Importa widgets do PyQt5

# Adiciona o diretório pai ao caminho de busca de módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class LojaApp(QWidget):  # Define a classe LojaApp que herda de QWidget
    # Método inicializador da classe
    def __init__(self, conexao, tab_loja_widget, main_window, usuario):
        # Chama o método inicializador da classe pai
        super(LojaApp, self).__init__()
        self.conexao = conexao  # Atribui a conexão ao atributo da classe
        self.tab_loja = tab_loja_widget  # Atribui o widget da tab ao atributo da classe
        self.main_window = main_window  # Atribui a janela principal ao atributo da classe
        self.usuario = usuario  # Atribui o usuário ao atributo da classe

        # Agora você pode acessar os widgets diretamente usando self.tab_loja
        self.txt_CodigoPesquisa = self.tab_loja.findChild(
            QLineEdit, "txt_CodigoPesquisa")  # Encontra o widget txt_CodigoPesquisa
        self.txt_CodigoLoja = self.tab_loja.findChild(
            QLineEdit, "txt_CodigoLoja")  # Encontra o widget txt_CodigoLoja
        self.txt_NomeLoja = self.tab_loja.findChild(
            QLineEdit, "txt_NomeLoja")  # Encontra o widget txt_NomeLoja
        self.txt_FoneLoja = self.tab_loja.findChild(
            QLineEdit, "txt_FoneLoja")  # Encontra o widget txt_FoneLoja
        self.txt_SiglaLoja = self.tab_loja.findChild(
            QLineEdit, "txt_SiglaLoja")  # Encontra o widget txt_SiglaLoja
        self.btn_Pesquisar = self.tab_loja.findChild(
            QPushButton, "btn_Pesquisar")  # Encontra o widget btn_Pesquisar
        self.btn_LojaInserir = self.tab_loja.findChild(
            QPushButton, "btn_LojaInserir")  # Encontra o widget btn_LojaInserir
        self.btn_LojaAtualizar = self.tab_loja.findChild(
            QPushButton, "btn_LojaAtualizar")  # Encontra o widget btn_LojaAtualizar
        self.btn_LojaApagar = self.tab_loja.findChild(
            QPushButton, "btn_LojaApagar")  # Encontra o widget btn_LojaApagar
        self.tableWidgetLoja = self.tab_loja.findChild(
            QTableWidget, "tableWidgetLoja")  # Encontra o widget tableWidgetLoja

        # Conecta os botões às funções
        # Conecta o botão btn_Pesquisar à função pesquisar_loja
        self.btn_Pesquisar.clicked.connect(self.pesquisar_loja)
        # Conecta o botão btn_LojaInserir à função inserir_loja
        self.btn_LojaInserir.clicked.connect(self.inserir_loja)
        # Conecta o botão btn_LojaAtualizar à função atualizar_loja
        self.btn_LojaAtualizar.clicked.connect(self.atualizar_loja)
        # Conecta o botão btn_LojaApagar à função apagar_loja
        self.btn_LojaApagar.clicked.connect(self.apagar_loja)
        # Conecta o evento cellClicked do tableWidgetLoja à função limpar_campos
        self.tableWidgetLoja.cellClicked.connect(self.limpar_campos)
        # Conecta o evento cellDoubleClicked do tableWidgetLoja à função preencher_campos
        self.tableWidgetLoja.cellDoubleClicked.connect(self.preencher_campos)

        # Conecta os eventos de saída dos campos para converter em maiúsculas
        self.txt_NomeLoja.editingFinished.connect(
            lambda: self.converter_para_maiusculas(self.txt_NomeLoja))
        self.txt_SiglaLoja.editingFinished.connect(
            lambda: self.converter_para_maiusculas(self.txt_SiglaLoja))

        self.atualizar_tabela()  # Chama a função atualizar_tabela

    def converter_para_maiusculas(self, campo):
        """Converte o texto do campo para maiúsculas."""
        texto = campo.text().strip().upper()
        campo.setText(texto)

    def pesquisar_loja(self):  # Define a função pesquisar_loja
        # Obtém o texto do widget txt_CodigoPesquisa e remove espaços em branco
        codigo = self.txt_CodigoPesquisa.text().strip()

        if not codigo:  # Verifica se o código está vazio
            # Exibe uma mensagem de aviso
            QMessageBox.warning(
                self, "Atenção", "Por favor, insira o código da loja para pesquisar.")
            return  # Retorna da função

        cursor = self.conexao.cursor()  # Obtém um cursor da conexão
        cursor.execute("SELECT * FROM lojas WHERE id=%s",
                       (codigo,))  # Executa a consulta SQL
        loja = cursor.fetchone()  # Obtém o primeiro resultado da consulta

        if loja:  # Verifica se a loja foi encontrada
            # Define o texto do widget txt_CodigoLoja
            self.txt_CodigoLoja.setText(str(loja[0]))
            # Define o texto do widget txt_NomeLoja
            self.txt_NomeLoja.setText(loja[1])
            # Define o texto do widget txt_FoneLoja
            self.txt_FoneLoja.setText(loja[2])
            # Define o texto do widget txt_SiglaLoja
            self.txt_SiglaLoja.setText(loja[3])
        else:  # Se a loja não foi encontrada
            # Exibe uma mensagem de erro
            QMessageBox.warning(self, "Erro", "Loja não encontrada.")

    def inserir_loja(self):  # Define a função inserir_loja
        try:
            # Obtém o texto do widget txt_CodigoLoja e converte para inteiro
            id = int(self.txt_CodigoLoja.text().strip())
        except ValueError:
            # Exibe uma mensagem de erro
            QMessageBox.warning(
                self, "Erro", "O código da loja deve ser um número inteiro.")
            return

        # Obtém o texto do widget txt_NomeLoja e remove espaços em branco
        loja = self.txt_NomeLoja.text().strip()
        # Obtém o texto do widget txt_FoneLoja e remove espaços em branco
        fone = self.txt_FoneLoja.text().strip()
        # Obtém o texto do widget txt_SiglaLoja e remove espaços em branco
        sigla = self.txt_SiglaLoja.text().strip()

        # Verifica se todos os campos estão preenchidos
        if not loja or not fone or not sigla:  # Verifica se algum campo está vazio
            # Exibe uma mensagem de aviso
            QMessageBox.warning(
                self, "Atenção", "Por favor, preencha todos os campos.")
            return  # Retorna da função

        # Verifica se a loja já existe no banco de dados
        cursor = self.conexao.cursor()
        cursor.execute(
            "SELECT * FROM lojas WHERE id=%s OR loja=%s OR fone=%s OR sigla=%s", (id, loja, fone, sigla))
        loja_existente = cursor.fetchone()

        if loja_existente:
            # Exibe uma mensagem de erro
            QMessageBox.warning(
                self, "Erro", "Já existe uma loja com um dos campos fornecidos.")
            self.limpar_campos()  # Limpa os campos do formulário
            return

        resposta = QMessageBox.question(self, "Confirmação", "Deseja realmente inserir esta loja?",  # Exibe uma mensagem de confirmação
                                        QMessageBox.Yes | QMessageBox.No)  # Define os botões da mensagem

        if resposta == QMessageBox.Yes:  # Verifica se a resposta foi "Sim"
            cursor.execute(
                # Executa a consulta SQL
                "INSERT INTO lojas (id, loja, fone, sigla) VALUES (%s, %s, %s, %s)", (id, loja, fone, sigla))
            self.conexao.commit()  # Confirma a transação

            # Exibe uma mensagem de sucesso
            QMessageBox.information(
                self, "Sucesso", "Loja inserida com sucesso")
            self.atualizar_tabela()  # Chama a função atualizar_tabela

    def atualizar_loja(self):  # Define a função atualizar_loja
        try:
            # Obtém o texto do widget txt_CodigoLoja e converte para inteiro
            id = int(self.txt_CodigoLoja.text().strip())
        except ValueError:
            # Exibe uma mensagem de erro
            QMessageBox.warning(
                self, "Erro", "O código da loja deve ser um número inteiro.")
            return

        # Obtém o texto do widget txt_NomeLoja e remove espaços em branco
        loja = self.txt_NomeLoja.text().strip()
        # Obtém o texto do widget txt_FoneLoja e remove espaços em branco
        fone = self.txt_FoneLoja.text().strip()
        # Obtém o texto do widget txt_SiglaLoja e remove espaços em branco
        sigla = self.txt_SiglaLoja.text().strip()

        resposta = QMessageBox.question(self, "Confirmação", "Deseja realmente atualizar esta loja?",  # Exibe uma mensagem de confirmação
                                        QMessageBox.Yes | QMessageBox.No)  # Define os botões da mensagem

        if resposta == QMessageBox.Yes:  # Verifica se a resposta foi "Sim"
            cursor = self.conexao.cursor()  # Obtém um cursor da conexão
            cursor.execute(
                # Executa a consulta SQL
                "UPDATE lojas SET loja=%s, fone=%s, sigla=%s WHERE id=%s", (id,loja, fone, sigla))
            self.conexao.commit()  # Confirma a transação

            if cursor.rowcount > 0:  # Verifica se alguma linha foi afetada
                # Exibe uma mensagem de sucesso
                QMessageBox.information(
                    self, "Sucesso", "Loja atualizada com sucesso")
            else:
                # Exibe uma mensagem de erro
                QMessageBox.warning(
                    self, "Erro", "Nenhuma loja encontrada com o código fornecido.")

            self.atualizar_tabela()  # Chama a função atualizar_tabela

    def apagar_loja(self):  # Define a função apagar_loja
        try:
            # Obtém o texto do widget txt_CodigoLoja e converte para inteiro
            id = int(self.txt_CodigoLoja.text().strip())
        except ValueError:
            # Exibe uma mensagem de erro
            QMessageBox.warning(
                self, "Erro", "O código da loja deve ser um número inteiro.")
            return

        resposta = QMessageBox.question(self, "Confirmação", "Deseja realmente apagar esta loja?",  # Exibe uma mensagem de confirmação
                                        QMessageBox.Yes | QMessageBox.No)  # Define os botões da mensagem

        if resposta == QMessageBox.Yes:  # Verifica se a resposta foi "Sim"
            cursor = self.conexao.cursor()  # Obtém um cursor da conexão
            cursor.execute("DELETE FROM lojas WHERE id=%s",
                           (id,))  # Executa a consulta SQL
            self.conexao.commit()  # Confirma a transação

            if cursor.rowcount > 0:  # Verifica se alguma linha foi afetada
                # Exibe uma mensagem de sucesso
                QMessageBox.information(
                    self, "Sucesso", "Loja apagada com sucesso")
            else:
                # Exibe uma mensagem de erro
                QMessageBox.warning(
                    self, "Erro", "Nenhuma loja encontrada com o código fornecido.")

            self.atualizar_tabela()  # Chama a função atualizar_tabela

    def limpar_campos(self, row=None, column=None):  # Define a função limpar_campos
        self.txt_CodigoLoja.clear()  # Limpa o texto do widget txt_CodigoLoja
        self.txt_NomeLoja.clear()  # Limpa o texto do widget txt_NomeLoja
        self.txt_FoneLoja.clear()  # Limpa o texto do widget txt_FoneLoja
        self.txt_SiglaLoja.clear()  # Limpa o texto do widget txt_SiglaLoja

    def preencher_campos(self, row, column):  # Define a função preencher_campos
        # Obtém o texto do item da tabela na linha e coluna especificadas
        id = self.tableWidgetLoja.item(row, 0).text()
        # Define o texto do widget txt_CodigoPesquisa
        self.txt_CodigoPesquisa.setText(id)
        self.pesquisar_loja()  # Chama a função pesquisar_loja

    def atualizar_tabela(self):  # Define a função atualizar_tabela
        cursor = self.conexao.cursor()  # Obtém um cursor da conexão
        # Executa a consulta SQL
        cursor.execute("SELECT * FROM lojas ORDER BY id ASC")
        lojas = cursor.fetchall()  # Obtém todos os resultados da consulta

        # Define o número de linhas da tabela como 0
        self.tableWidgetLoja.setRowCount(0)
        # Itera sobre os resultados da consulta
        for row_number, row_data in enumerate(lojas):
            # Insere uma nova linha na tabela
            self.tableWidgetLoja.insertRow(row_number)
            # Itera sobre os dados da linha
            for column_number, data in enumerate(row_data):
                self.tableWidgetLoja.setItem(
                    # Define o item da tabela na linha e coluna especificadas
                    row_number, column_number, QTableWidgetItem(str(data)))


if __name__ == "__main__":  # Verifica se o script está sendo executado diretamente
    # Cria uma instância da aplicação QApplication
    app = QApplication(sys.argv)
    # Cria uma instância da classe LojaApp com parâmetros fictícios
    window = LojaApp(None, None, None, None)
    window.show()  # Exibe a janela
    sys.exit(app.exec_())  # Executa a aplicação e aguarda o sinal de saída
