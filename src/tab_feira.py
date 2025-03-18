from Banco import database  # Importa a conexão com o banco
import sys
import os
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QApplication, QLineEdit, QPushButton, QTableWidget, QDateEdit
from PyQt5.QtCore import QDate
import mysql.connector
from datetime import date  # Importa a classe date do módulo datetime

# Ajusta o caminho do projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TabFeira(QWidget):
    def __init__(self, conexao, tab_feira, main_window, usuario):
        super(TabFeira, self).__init__()
        self.conexao = conexao  # Conexão com MySQL
        self.tab_feira = tab_feira  # Referência à aba
        self.main_window = main_window  # Referência à janela principal
        self.usuario = usuario  # Usuário logado

        # Inicializa os widgets
        self.txt_NomeFeira_pesquisa = self.tab_feira.findChild(
            QLineEdit, "txt_NomeFeira_pesquisa")
        self.txt_Nome_Feira = self.tab_feira.findChild(
            QLineEdit, "txt_Nome_Feira")
        self.dateEdit_inicio = self.tab_feira.findChild(
            QDateEdit, "dateEdit_inicio")
        self.txt_Feira_Sigla = self.tab_feira.findChild(
            QLineEdit, "txt_Feira_Sigla")
        self.btn_Pesquisar_feira = self.tab_feira.findChild(
            QPushButton, "btn_Pesquisar_feira")
        self.btn_Feira_Inserir = self.tab_feira.findChild(
            QPushButton, "btn_Feira_Inserir")
        self.btn_Feira_Atualizar = self.tab_feira.findChild(
            QPushButton, "btn_Feira_Atualizar")
        self.btn_Feira_Apagar = self.tab_feira.findChild(
            QPushButton, "btn_Feira_Apagar")
        self.tableWidget_Feira = self.tab_feira.findChild(
            QTableWidget, "tableWidget_Feira")

        # Conecta os botões às funções
        self.btn_Pesquisar_feira.clicked.connect(self.pesquisar_feira)
        self.btn_Feira_Inserir.clicked.connect(self.inserir_feira)
        self.btn_Feira_Atualizar.clicked.connect(self.atualizar_feira)
        self.btn_Feira_Apagar.clicked.connect(self.apagar_feira)
        self.tableWidget_Feira.cellClicked.connect(self.limpar_campos)
        self.tableWidget_Feira.cellDoubleClicked.connect(self.preencher_campos)

        # Conecta os eventos de saída dos campos para converter em maiúsculas
        self.txt_NomeFeira_pesquisa.editingFinished.connect(
            lambda: self.converter_para_maiusculas(self.txt_NomeFeira_pesquisa))
        self.txt_Nome_Feira.editingFinished.connect(
            lambda: self.converter_para_maiusculas(self.txt_Nome_Feira))
        self.txt_Feira_Sigla.editingFinished.connect(
            lambda: self.converter_para_maiusculas(self.txt_Feira_Sigla))

        # Atualiza a tabela ao iniciar
        self.atualizar_tabela()

    def converter_para_maiusculas(self, campo):
        """Converte o texto do campo para maiúsculas."""
        texto = campo.text().strip().upper()
        campo.setText(texto)

    def formatar_data(self, data):
        """Formata a data para exibição."""
        return data.strftime('%d/%m/%Y') if isinstance(data, date) else ''

    def set_date_edit(self, date_widget, data):
        """Define a data no QDateEdit."""
        if isinstance(data, date):
            data_qdate = QDate.fromString(
                data.strftime('%d/%m/%Y'), "dd/MM/yyyy")
            if date_widget:
                date_widget.setDate(data_qdate)
        else:
            if date_widget:
                date_widget.setDate(QDate.currentDate())

    def pesquisar_feira(self):
        """Pesquisa uma feira pelo nome ou parte do nome e preenche os campos correspondentes."""
        nome_feira = self.txt_NomeFeira_pesquisa.text().strip().upper()
        print(f"Pesquisando feira: {nome_feira}")

        if not nome_feira:
            QMessageBox.warning(
                self, "Atenção", "Por favor, insira o nome da feira para pesquisar.")
            return

        cursor = self.conexao.cursor()
        cursor.execute(
            "SELECT * FROM feira WHERE nome_feira LIKE %s", (f"%{nome_feira}%",))
        feira = cursor.fetchone()

        if feira:
            print(f"Feira encontrada: {feira}")
            self.txt_Nome_Feira.setText(feira[1])
            # Define a data de início
            self.set_date_edit(self.dateEdit_inicio, feira[2])
            self.txt_Feira_Sigla.setText(feira[3])
        else:
            print("Feira não encontrada.")
            QMessageBox.warning(
                self, "Erro", "Nenhuma feira encontrada com o nome fornecido.")
            self.limpar_campos()

    def inserir_feira(self):
        """Insere uma nova feira no banco de dados."""
        nome_feira = self.txt_Nome_Feira.text().strip().upper()
        data_inicio = self.dateEdit_inicio.date().toString(
            'yyyy-MM-dd') if self.dateEdit_inicio else None
        sigla_feira = self.txt_Feira_Sigla.text().strip()
        print(f"Inserindo feira: {nome_feira}, {data_inicio}, {sigla_feira}")

        if not nome_feira or not data_inicio or not sigla_feira:
            QMessageBox.warning(
                self, "Atenção", "Por favor, preencha todos os campos.")
            return

        resposta = QMessageBox.question(self, "Confirmação", "Deseja realmente inserir esta feira?",
                                        QMessageBox.Yes | QMessageBox.No)

        if resposta == QMessageBox.Yes:
            cursor = self.conexao.cursor()
            cursor.execute("INSERT INTO feira (nome_feira, data_inicio, sigla_feira) VALUES (%s, %s, %s)",
                           (nome_feira, data_inicio, sigla_feira))
            self.conexao.commit()
            cursor.close()

            QMessageBox.information(
                self, "Sucesso", "Feira inserida com sucesso!")
            self.atualizar_tabela()
            self.limpar_campos()

    def atualizar_feira(self):
        """Atualiza uma feira existente no banco de dados."""
        nome_feira = self.txt_Nome_Feira.text().strip().upper()
        data_inicio = self.dateEdit_inicio.date().toString(
            'yyyy-MM-dd') if self.dateEdit_inicio else None
        sigla_feira = self.txt_Feira_Sigla.text().strip()
        print(f"Atualizando feira: {nome_feira}, {data_inicio}, {sigla_feira}")

        if not nome_feira or not data_inicio or not sigla_feira:
            QMessageBox.warning(
                self, "Atenção", "Por favor, preencha todos os campos.")
            return

        resposta = QMessageBox.question(self, "Confirmação", "Deseja realmente atualizar esta feira?",
                                        QMessageBox.Yes | QMessageBox.No)

        if resposta == QMessageBox.Yes:
            cursor = self.conexao.cursor()
            cursor.execute("UPDATE feira SET data_inicio = %s, sigla_feira = %s WHERE nome_feira = %s",
                           (data_inicio, sigla_feira, nome_feira))
            self.conexao.commit()

            if cursor.rowcount > 0:
                QMessageBox.information(
                    self, "Sucesso", "Feira atualizada com sucesso!")
            else:
                QMessageBox.warning(
                    self, "Erro", "Nenhuma feira encontrada com o nome fornecido.")

            cursor.close()
            self.atualizar_tabela()
            self.limpar_campos()

    def apagar_feira(self):
        """Apaga uma feira do banco de dados."""
        nome_feira = self.txt_Nome_Feira.text().strip()
        print(f"Apagando feira: {nome_feira}")

        if not nome_feira:
            QMessageBox.warning(
                self, "Atenção", "Selecione uma feira para apagar.")
            return

        resposta = QMessageBox.question(self, "Confirmação", "Deseja realmente apagar esta feira?",
                                        QMessageBox.Yes | QMessageBox.No)

        if resposta == QMessageBox.Yes:
            cursor = self.conexao.cursor()
            cursor.execute(
                "DELETE FROM feira WHERE nome_feira = %s", (nome_feira,))
            self.conexao.commit()
            cursor.close()

            if cursor.rowcount > 0:  # Verifica se alguma linha foi afetada
                QMessageBox.information(
                    self, "Sucesso", "Feira apagada com sucesso!")
            else:
                QMessageBox.warning(
                    self, "Erro", "Nenhuma feira encontrada com o nome fornecido.")

            self.atualizar_tabela()
            self.limpar_campos()

    def atualizar_tabela(self):
        """Atualiza a tabela de feiras."""
        print("Atualizando tabela de feiras")
        cursor = self.conexao.cursor()
        cursor.execute(
            "SELECT id, nome_feira, data_inicio, sigla_feira FROM feira ORDER BY nome_feira ASC")
        feiras = cursor.fetchall()
        cursor.close()

        self.tableWidget_Feira.setRowCount(len(feiras))
        self.tableWidget_Feira.setColumnCount(4)
        self.tableWidget_Feira.setHorizontalHeaderLabels(
            ["ID", "Nome Feira", "Data Início", "Sigla Feira"])

        for i, (id, nome_feira, data_inicio, sigla_feira) in enumerate(feiras):
            data_inicio_str = self.formatar_data(data_inicio)
            self.tableWidget_Feira.setItem(i, 0, QTableWidgetItem(str(id)))
            self.tableWidget_Feira.setItem(i, 1, QTableWidgetItem(nome_feira))
            self.tableWidget_Feira.setItem(
                i, 2, QTableWidgetItem(data_inicio_str))
            self.tableWidget_Feira.setItem(i, 3, QTableWidgetItem(sigla_feira))

    def preencher_campos(self, row, column):
        """Preenche os campos do formulário com os dados da linha selecionada na tabela."""
        print(f"Preenchendo campos da linha: {row}")
        nome_feira = self.tableWidget_Feira.item(row, 1).text()
        cursor = self.conexao.cursor()
        cursor.execute(
            "SELECT * FROM feira WHERE nome_feira = %s", (nome_feira,))
        feira = cursor.fetchone()
        cursor.close()

        if feira:
            self.txt_Nome_Feira.setText(feira[1])
            self.set_date_edit(self.dateEdit_inicio, feira[2])
            self.txt_Feira_Sigla.setText(feira[3])
        else:
            QMessageBox.warning(
                self, "Erro", "Erro ao buscar dados da feira no banco de dados.")

    def limpar_campos(self):
        """Limpa os campos do formulário."""
        print("Limpando campos do formulário")
        self.txt_NomeFeira_pesquisa.clear()
        self.txt_Nome_Feira.clear()
        if self.dateEdit_inicio:
            self.dateEdit_inicio.setDate(QDate.currentDate())
        self.txt_Feira_Sigla.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    conexao = database.connect()  # Substitua pelo objeto de conexão real
    tab_feira_widget = None  # Substitua pelo widget real
    main_window = None  # Substitua pela janela principal real
    usuario = None  # Substitua pelo usuário real
    window = TabFeira(conexao, tab_feira_widget, main_window, usuario)
    window.show()
    sys.exit(app.exec_())
