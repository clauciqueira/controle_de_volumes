# -*- coding: utf-8 -*-
# TabRelatorio.py

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QCheckBox, QMainWindow, QDateEdit
from PyQt5.QtCore import Qt, QDate, QRectF, QPoint
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPainter, QFont, QRegion

from Banco import database
from Doc import utils
from datetime import datetime, date
import os
import locale
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
 
from reportlab.lib.units import inch  
from reportlab.platypus import Table, TableStyle  
from reportlab.lib import colors  
import os  



locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class TabRelatorio(QWidget):
    def __init__(self, conexao, tab_relatorio_widget):  # Removido main_window
        super().__init__()
        self.conexao = conexao
        self.tab_relatorio = tab_relatorio_widget
        # Encontre os widgets
        self.txt_PesquisarLoja = self.tab_relatorio.findChild(
            QLineEdit, "txt_PesquisarLoja")
        self.txt_PesquisarUsuario = self.tab_relatorio.findChild(
            QLineEdit, "txt_PesquisarUsuario")
        self.txt_PesquisarOrcamento = self.tab_relatorio.findChild(
            QLineEdit, "txt_PesquisarOrcamento")
        self.txt_PesquisarFeira = self.tab_relatorio.findChild(
            QLineEdit, "txt_PesquisarFeira")
        self.txt_PesquisarQuantidade = self.tab_relatorio.findChild(
            QLineEdit, "txt_PesquisarQuantidade")
        self.dateEdit_PesquisarData = self.tab_relatorio.findChild(
            QDateEdit, "dateEdit_PesquisarData")
        self.dateEdit_PesquisarEnvio = self.tab_relatorio.findChild(
            QDateEdit, "dateEdit_PesquisarEnvio")

        self.checkBoxLoja = self.tab_relatorio.findChild(
            QCheckBox, "checkBoxLoja")
        self.checkBoxUsuario = self.tab_relatorio.findChild(
            QCheckBox, "checkBoxUsuario")
        self.checkBoxOrcamento = self.tab_relatorio.findChild(
            QCheckBox, "checkBoxOrcamento")
        self.checkBoxFeira = self.tab_relatorio.findChild(
            QCheckBox, "checkBoxFeira")
        self.checkBoxQquantidade = self.tab_relatorio.findChild(
            QCheckBox, "checkBoxQquantidade")
        self.checkBoxData = self.tab_relatorio.findChild(
            QCheckBox, "checkBoxData")
        self.checkBoxEnvio = self.tab_relatorio.findChild(
            QCheckBox, "checkBoxEnvio")

        self.tableWidgetPesquisa = self.tab_relatorio.findChild(
            QTableWidget, "tableWidgetPesquisa")
        self.btnPesquisa = self.tab_relatorio.findChild(
            QPushButton, "btnPesquisa")
        self.btnPesquisa_Imprimir = self.tab_relatorio.findChild(
            QPushButton, "btnPesquisa_Imprimir")

        # Configurações da tabela
        self.tableWidgetPesquisa.setEditTriggers(
            QAbstractItemView.NoEditTriggers)
        self.tableWidgetPesquisa.setSelectionBehavior(
            QAbstractItemView.SelectRows)
        self.tableWidgetPesquisa.setSelectionMode(
            QAbstractItemView.SingleSelection)
        self.tableWidgetPesquisa.horizontalHeader(
        ).setSectionResizeMode(QHeaderView.Stretch)

        # Desabilitar campos de texto e data inicialmente
        self.txt_PesquisarLoja.setEnabled(False)
        self.txt_PesquisarUsuario.setEnabled(False)
        self.txt_PesquisarOrcamento.setEnabled(False)
        self.txt_PesquisarFeira.setEnabled(False)
        self.txt_PesquisarQuantidade.setEnabled(False)
        self.dateEdit_PesquisarData.setEnabled(False)
        self.dateEdit_PesquisarEnvio.setEnabled(False)

        # Conectar checkboxes para habilitar/desabilitar campos
        self.checkBoxLoja.toggled.connect(
            lambda: self.txt_PesquisarLoja.setEnabled(self.checkBoxLoja.isChecked()))
        self.checkBoxUsuario.toggled.connect(
            lambda: self.txt_PesquisarUsuario.setEnabled(self.checkBoxUsuario.isChecked()))
        self.checkBoxOrcamento.toggled.connect(
            lambda: self.txt_PesquisarOrcamento.setEnabled(self.checkBoxOrcamento.isChecked()))
        self.checkBoxFeira.toggled.connect(
            lambda: self.txt_PesquisarFeira.setEnabled(self.checkBoxFeira.isChecked()))
        self.checkBoxQquantidade.toggled.connect(
            lambda: self.txt_PesquisarQuantidade.setEnabled(self.checkBoxQquantidade.isChecked()))
        self.checkBoxData.toggled.connect(
            lambda: self.dateEdit_PesquisarData.setEnabled(self.checkBoxData.isChecked()))
        self.checkBoxEnvio.toggled.connect(
            lambda: self.dateEdit_PesquisarEnvio.setEnabled(self.checkBoxEnvio.isChecked()))

        # Conectar eventos de saída dos campos para converter em maiúsculas
        self.txt_PesquisarLoja.editingFinished.connect(
            lambda: self.converter_para_maiusculas(self.txt_PesquisarLoja))
        self.txt_PesquisarUsuario.editingFinished.connect(
            lambda: self.converter_para_maiusculas(self.txt_PesquisarUsuario))
        self.txt_PesquisarOrcamento.editingFinished.connect(
            lambda: self.converter_para_maiusculas(self.txt_PesquisarOrcamento))
        self.txt_PesquisarFeira.editingFinished.connect(
            lambda: self.converter_para_maiusculas(self.txt_PesquisarFeira))
        self.txt_PesquisarQuantidade.editingFinished.connect(
            lambda: self.converter_para_maiusculas(self.txt_PesquisarQuantidade))

        # Conecte os sinais dos botões aos slots apropriados
        self.btnPesquisa.clicked.connect(self.executar_pesquisa)
        self.btnPesquisa_Imprimir.clicked.connect(self.imprimir_relatorio)

        # Inicializar campos de data com a data atual
        self.dateEdit_PesquisarData.setDate(QDate.currentDate())
        self.dateEdit_PesquisarEnvio.setDate(QDate.currentDate())

    def converter_para_maiusculas(self, campo):
        """Converte o texto do campo para maiúsculas."""
        texto = campo.text().strip().upper()
        campo.setText(texto)

    def carregar_dados(self):
        """
        Carrega os dados na tableWidgetPesquisa, ordenando por Orçamento decrescente.
        """
        self.tableWidgetPesquisa.clear()  # Limpa a tabela antes de carregar os dados
        self.tableWidgetPesquisa.setRowCount(0)  # Reseta o número de linhas

        query = "SELECT id, loja, usuario, orcamento, quantidade, feira, data, data_envio FROM volumes ORDER BY orcamento DESC"
        resultados = database.executar_query_retorno(self.conexao, query)

        if resultados:
            # Define o número de colunas na tabela
            self.tableWidgetPesquisa.setColumnCount(
                8)  # Ajuste conforme necessário

            # Define o cabeçalho da tabela
            self.tableWidgetPesquisa.setHorizontalHeaderLabels(
                # Ajuste conforme necessário
                ["ID", "Loja", "Usuário", "Orçamento", "Quantidade", "Feira", "Data", "Data Envio"])

            for volume in resultados:
                id, loja, usuario, orcamento, quantidade, feira, data, data_envio = volume

                # Formata as datas para exibição
                data = data.strftime(
                    '%d/%m/%Y') if isinstance(data, date) else ''
                data_envio = data_envio.strftime(
                    '%d/%m/%Y') if data_envio and isinstance(data_envio, date) else ''

                # Adiciona uma nova linha na tabela
                row_position = self.tableWidgetPesquisa.rowCount()
                self.tableWidgetPesquisa.insertRow(row_position)

                # Preenche as células da linha com os dados do volume
                self.tableWidgetPesquisa.setItem(
                    row_position, 0, QTableWidgetItem(str(id)))
                self.tableWidgetPesquisa.setItem(
                    row_position, 1, QTableWidgetItem(loja))
                self.tableWidgetPesquisa.setItem(
                    row_position, 2, QTableWidgetItem(usuario))
                self.tableWidgetPesquisa.setItem(
                    row_position, 3, QTableWidgetItem(orcamento))
                self.tableWidgetPesquisa.setItem(
                    row_position, 4, QTableWidgetItem(str(quantidade)))
                self.tableWidgetPesquisa.setItem(
                    row_position, 5, QTableWidgetItem(feira))
                self.tableWidgetPesquisa.setItem(
                    row_position, 6, QTableWidgetItem(data))
                self.tableWidgetPesquisa.setItem(
                    row_position, 7, QTableWidgetItem(data_envio))

            # Ajusta o tamanho das colunas para o conteúdo
            self.tableWidgetPesquisa.resizeColumnsToContents()

        else:
            utils.mostrar_mensagem(
                "Informação", "Nenhum volume encontrado.", QMessageBox.Information)

    def executar_pesquisa(self):
        """
        Executa a pesquisa com base nos critérios selecionados e exibe os resultados na tabela.
        """
        criterios = []
        valores = []
        if self.checkBoxLoja.isChecked() and len(self.txt_PesquisarLoja.text().strip()) >= 3:
            criterios.append("loja LIKE %s")
            valores.append(f"%{self.txt_PesquisarLoja.text().strip()}%")
        if self.checkBoxUsuario.isChecked() and len(self.txt_PesquisarUsuario.text().strip()) >= 3:
            criterios.append("usuario LIKE %s")
            valores.append(f"%{self.txt_PesquisarUsuario.text().strip()}%")
        if self.checkBoxOrcamento.isChecked() and len(self.txt_PesquisarOrcamento.text().strip()) >= 3:
            criterios.append("orcamento LIKE %s")
            valores.append(f"%{self.txt_PesquisarOrcamento.text().strip()}%")
        if self.checkBoxFeira.isChecked() and len(self.txt_PesquisarFeira.text().strip()) >= 3:
            criterios.append("feira LIKE %s")
            valores.append(f"%{self.txt_PesquisarFeira.text().strip()}%")
        if self.checkBoxQquantidade.isChecked() and self.txt_PesquisarQuantidade.text().strip().isdigit():
            criterios.append("quantidade = %s")
            valores.append(self.txt_PesquisarQuantidade.text().strip())
        if self.checkBoxData.isChecked():
            criterios.append("data LIKE %s")
            valores.append(
                f"%{self.dateEdit_PesquisarData.date().toString('yyyy-MM-dd')}%")
        if self.checkBoxEnvio.isChecked():
            criterios.append("data_envio LIKE %s")
            valores.append(
                f"%{self.dateEdit_PesquisarEnvio.date().toString('yyyy-MM-dd')}%")

        query = "SELECT id, loja, usuario, orcamento, quantidade, feira, data, data_envio FROM volumes"
        if criterios:
            query += " WHERE " + " AND ".join(criterios)
        query += " ORDER BY orcamento DESC"

        try:
            cursor = self.conexao.cursor()
            cursor.execute(query, valores)
            resultados = cursor.fetchall()
        except Exception as e:
            utils.mostrar_mensagem(
                "Erro", f"Erro ao executar pesquisa: {str(e)}", QMessageBox.Critical)
            return

        self.preencher_tabela(resultados)
        self.limpar_campos()

    def preencher_tabela(self, resultados):
        """
        Preenche a tabela com os resultados da pesquisa e calcula a soma das quantidades.
        """
        self.tableWidgetPesquisa.clear()
        self.tableWidgetPesquisa.setRowCount(0)
        self.tableWidgetPesquisa.setColumnCount(8)
        self.tableWidgetPesquisa.setHorizontalHeaderLabels(
            ["ID", "Loja", "Usuário", "Orçamento", "Quantidade", "Feira", "Data", "Data Envio"])

        soma_quantidades = 0
        for volume in resultados:
            id, loja, usuario, orcamento, quantidade, feira, data, data_envio = volume

            data = data.strftime('%d/%m/%Y') if isinstance(data, date) else ''
            data_envio = data_envio.strftime(
                '%d/%m/%Y') if data_envio and isinstance(data_envio, date) else ''

            row_position = self.tableWidgetPesquisa.rowCount()
            self.tableWidgetPesquisa.insertRow(row_position)

            self.tableWidgetPesquisa.setItem(
                row_position, 0, QTableWidgetItem(str(id)))
            self.tableWidgetPesquisa.setItem(
                row_position, 1, QTableWidgetItem(loja))
            self.tableWidgetPesquisa.setItem(
                row_position, 2, QTableWidgetItem(usuario))
            self.tableWidgetPesquisa.setItem(
                row_position, 3, QTableWidgetItem(orcamento))
            self.tableWidgetPesquisa.setItem(
                row_position, 4, QTableWidgetItem(str(quantidade)))
            self.tableWidgetPesquisa.setItem(
                row_position, 5, QTableWidgetItem(feira))
            self.tableWidgetPesquisa.setItem(
                row_position, 6, QTableWidgetItem(data))
            self.tableWidgetPesquisa.setItem(
                row_position, 7, QTableWidgetItem(data_envio))

            soma_quantidades += quantidade

        # Adiciona a linha de total
        row_position = self.tableWidgetPesquisa.rowCount()
        self.tableWidgetPesquisa.insertRow(row_position)
        self.tableWidgetPesquisa.setItem(
            row_position, 0, QTableWidgetItem("Total"))
        self.tableWidgetPesquisa.setItem(
            row_position, 4, QTableWidgetItem(str(soma_quantidades)))

        self.tableWidgetPesquisa.resizeColumnsToContents()

    def limpar_campos(self):
        """Limpa os campos de pesquisa."""
        self.txt_PesquisarLoja.clear()
        self.txt_PesquisarUsuario.clear()
        self.txt_PesquisarOrcamento.clear()
        self.txt_PesquisarFeira.clear()
        self.txt_PesquisarQuantidade.clear()
        self.dateEdit_PesquisarData.setDate(QDate.currentDate())
        self.dateEdit_PesquisarEnvio.setDate(QDate.currentDate())


    def desenhar_conteudo_pdf(self, c, titulo):  
        """Desenha o conteúdo do tableWidgetPesquisa em um PDF usando reportlab,  
        criando uma nova página a cada 50 itens.  
        """  
        width, height = A4  # Tamanho da página A4 em pontos  
        margin = 28.35  # 1 cm em pontos (1 cm = 28.35 pontos)  
        itens_por_pagina = 50  
        itens_na_pagina = 0  
        y = height - 160  # Define a posição inicial para os dados  

        def desenhar_cabecalho_rodape(canvas):  
            """Desenha o cabeçalho e rodapé em cada página."""  
            # Cabeçalho  
            canvas.setFont("Helvetica-Bold", 14)  
            canvas.drawString(50, height - 50, "CD Clip Serafina Corrêa")  
            canvas.line(50, height - 55, width - 50, height - 55)  

            # Título do Relatório  
            canvas.setFont("Helvetica-Bold", 16)  
            canvas.drawCentredString(width / 2.0, height - 100, titulo)  

            # Data  
            canvas.setFont("Helvetica", 10)  
            canvas.drawString(50, height - 120,  
                                f"Data: {datetime.now().strftime('%d/%m/%Y')}")  
            canvas.drawRightString(width - 50, height - 120,  
                                "Relatório Gerado Automaticamente")  

            # Rodapé personalizado  
            canvas.setFont("Helvetica", 10)  
            canvas.drawString(margin, margin, "Libélula Art String")  

        def criar_nova_pagina(canvas):  
            """Cria uma nova página e desenha o cabeçalho e rodapé."""  
            canvas.showPage()  
            desenhar_cabecalho_rodape(canvas)  
            return height - 160  # Retorna a posição Y inicial para a nova página  

        # Desenha o cabeçalho e rodapé na primeira página  
        desenhar_cabecalho_rodape(c)  

        # Calcular larguras de colunas  
        column_widths = []  
        for column in range(self.tableWidgetPesquisa.columnCount()):  
            max_width = c.stringWidth(self.tableWidgetPesquisa.horizontalHeaderItem(  
                column).text(), "Helvetica", 10) + 10  
            for row in range(self.tableWidgetPesquisa.rowCount()):  
                item = self.tableWidgetPesquisa.item(row, column)  
                if item:  
                    item_width = c.stringWidth(  
                        item.text(), "Helvetica", 10) + 10  
                    max_width = max(max_width, item_width)  
            column_widths.append(max_width)  

        # Cabeçalhos das colunas  
        c.setFont("Helvetica", 10)  
        y -= 20  # Ajusta posição vertical após cabeçalhos  
        for column in range(self.tableWidgetPesquisa.columnCount()):  
            item = self.tableWidgetPesquisa.horizontalHeaderItem(column)  
            if item is not None:  
                x = margin + sum(column_widths[:column])  
                c.drawString(x, y, item.text())  
        y -= 20  # Ajusta posição vertical após cabeçalhos  

        # Preencher dados da tabela  
        c.setFont("Helvetica", 10)  
        for row in range(self.tableWidgetPesquisa.rowCount()):  
            # Verificar se é necessário criar uma nova página  
            if itens_na_pagina >= itens_por_pagina or y < 2 * margin:  
                y = criar_nova_pagina(c)  
                itens_na_pagina = 0  

                # Desenhar novamente os cabeçalhos das colunas na nova página  
                c.setFont("Helvetica", 10)  
                for column in range(self.tableWidgetPesquisa.columnCount()):  
                    item = self.tableWidgetPesquisa.horizontalHeaderItem(column)  
                    if item is not None:  
                        x = margin + sum(column_widths[:column])  
                        c.drawString(x, y, item.text())  
                y -= 20  # Ajusta posição vertical após cabeçalhos  

            for column in range(self.tableWidgetPesquisa.columnCount()):  
                item = self.tableWidgetPesquisa.item(row, column)  
                if item is not None:  
                    x = margin + sum(column_widths[:column])  
                    c.drawString(x, y, item.text())  

            y -= 20  # Ajusta a posição vertical para a próxima linha  
            itens_na_pagina += 1  

            # Linha de separação para cada linha de dados  
            c.line(margin, y + 10, width - margin, y + 10)  

        # Finaliza a última página, se necessário  
        c.showPage()  
  


    def imprimir_relatorio(self):
        """
        Imprime o conteúdo do tableWidgetPesquisa para um arquivo PDF usando reportlab.
        """
        diretorio_salvar = "relatorios"
        if not os.path.exists(diretorio_salvar):
            os.makedirs(diretorio_salvar)

        # Determinar o nome do arquivo e o título do relatório com base no campo pesquisado
        nome_arquivo_base = "relatorio"
        titulo = "Relatório Geral"
        if self.checkBoxLoja.isChecked() and self.txt_PesquisarLoja.text().strip():
            nome_arquivo_base = self.txt_PesquisarLoja.text().strip()
            titulo = f"Relatório da Loja: {nome_arquivo_base}"
        elif self.checkBoxUsuario.isChecked() and self.txt_PesquisarUsuario.text().strip():
            nome_arquivo_base = self.txt_PesquisarUsuario.text().strip()
            titulo = f"Relatório do Usuário: {nome_arquivo_base}"
        elif self.checkBoxOrcamento.isChecked() and self.txt_PesquisarOrcamento.text().strip():
            nome_arquivo_base = self.txt_PesquisarOrcamento.text().strip()
            titulo = f"Relatório do Orçamento: {nome_arquivo_base}"
        elif self.checkBoxFeira.isChecked() and self.txt_PesquisarFeira.text().strip():
            nome_arquivo_base = self.txt_PesquisarFeira.text().strip()
            titulo = f"Relatório da Feira: {nome_arquivo_base}"
        elif self.checkBoxQquantidade.isChecked() and self.txt_PesquisarQuantidade.text().strip():
            nome_arquivo_base = self.txt_PesquisarQuantidade.text().strip()
            titulo = f"Relatório da Quantidade: {nome_arquivo_base}"
        elif self.checkBoxData.isChecked():
            nome_arquivo_base = self.dateEdit_PesquisarData.date().toString('dd-MM-yyyy')
            titulo = f"Relatório da Data: {nome_arquivo_base}"
        elif self.checkBoxEnvio.isChecked():
            nome_arquivo_base = self.dateEdit_PesquisarEnvio.date().toString('dd-MM-yyyy')
            titulo = f"Relatório da Data de Envio: {nome_arquivo_base}"

        nome_arquivo = os.path.join(
            diretorio_salvar, f"{nome_arquivo_base}.pdf")

        c = canvas.Canvas(nome_arquivo, pagesize=A4)
        self.desenhar_conteudo_pdf(c, titulo)
        c.save()

        utils.mostrar_mensagem(
            "Sucesso", "Relatório salvo com sucesso!", QMessageBox.Information)

        # Abrir o PDF após salvar
        os.startfile(nome_arquivo)
