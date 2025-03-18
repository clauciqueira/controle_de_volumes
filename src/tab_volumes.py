# -*- coding: utf-8 -*-
# tab_volumes.py
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox, QTreeWidgetItem, QLineEdit, QPushButton, QSpinBox, QTreeWidget, QDateEdit, QComboBox
from PyQt5.QtCore import QDate, Qt, pyqtSlot
import subprocess  # Importa o módulo subprocess para abrir arquivos externos

from Banco import database  # Importa o módulo database
from Doc import utils  # Importa o módulo utils
from datetime import datetime, date

import platform
import logging


# Configuração básica do logging
logging.basicConfig(filename='impressao_etiquetas.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class TabVolumes(QWidget):
    def __init__(self, conexao, tab_volume_widget, main_window, usuario):
        super(TabVolumes, self).__init__()
        self.conexao = conexao
        self.tab_volume = tab_volume_widget  # Referencia da tab
        self.main_window = main_window  # Referencia a main_window
        self.usuario = usuario  # Recebe o usuario

        # Agora você pode acessar os widgets diretamente usando self.tab_volume
        self.dateEdit_data = self.tab_volume.findChild(
            QDateEdit, "dateEdit_data")
        self.txt_usuarioVolume = self.tab_volume.findChild(
            QLineEdit, "txt_UsuarioVolume")
        self.txt_orcamentoVolume = self.tab_volume.findChild(
            QLineEdit, "txt_OrcamentoVolume")
        self.comboBox_feira = self.tab_volume.findChild(
            QComboBox, "comboBox_feira")
        self.txt_CodigoPesquisavolume = self.tab_volume.findChild(
            QLineEdit, "txt_CodigoPesquisavolume")
        self.comboBox_loja = self.tab_volume.findChild(
            QComboBox, "comboBox_loja")
        self.spinBoxVolume = self.tab_volume.findChild(
            QSpinBox, "spinBoxVolume")
        self.treeWidget = self.tab_volume.findChild(QTreeWidget, "treeWidget")
        # Supondo que comboBox seja o nome do combobox
        self.comboBox = self.tab_volume.findChild(QComboBox, "comboBox")

        self.btn_PesquisarVolume = self.tab_volume.findChild(
            QPushButton, "btn_PesquisarVolume")
        self.btn_InserirVolume = self.tab_volume.findChild(
            QPushButton, "btn_InserirVolume")
        self.btn_AtualizarVolume = self.tab_volume.findChild(
            QPushButton, "btn_AtualizarVolume")
        self.btn_ApagarVolume = self.tab_volume.findChild(
            QPushButton, "btn_ApagarVolume")
        self.btn_Imprimir_Etiquetas = self.tab_volume.findChild(
            QPushButton, "btn_Imprimir_Etiquetas")
        self.btn_envioVolume = self.tab_volume.findChild(
            QPushButton, "btn_envioVolume")  # Novo botão
        self.btn_cancelarVolume = self.tab_volume.findChild(
            QPushButton, "btn_cancelarVolume")  # Botão para cancelar envio

        # Verifique se os widgets foram encontrados
        if self.dateEdit_data is None:
            print("Erro: dateEdit_data não encontrado no main.ui!")
        else:
            self.dateEdit_data.setDisplayFormat("dd/MM/yyyy")
            self.dateEdit_data.setDate(QDate.currentDate())
            # Permite selecionar a data através de um calendário
            self.dateEdit_data.setCalendarPopup(True)
            # Define o foco no dateEdit_data ao inicializar a aba
            self.dateEdit_data.setFocus()

        if self.txt_usuarioVolume is None:
            print("Erro: txt_UsuarioVolume não encontrado no main.ui!")
        # Adicione verificações para todos os outros widgets também

        # Conecta os botões às funções
        self.btn_PesquisarVolume.clicked.connect(self.pesquisar_volume)
        self.btn_InserirVolume.clicked.connect(self.inserir_volume)
        self.btn_AtualizarVolume.clicked.connect(self.atualizar_volume)
        self.btn_ApagarVolume.clicked.connect(self.apagar_volume)
        self.btn_Imprimir_Etiquetas.clicked.connect(self.imprimir_etiquetas)
        self.btn_envioVolume.clicked.connect(
            self.atualizar_data_envio)  # Conecta o novo botão
        self.btn_cancelarVolume.clicked.connect(
            self.cancelar_envio)  # Conecta o botão cancelar envio

        self.carregar_volumes()  # Carrega os volumes ao iniciar a aba
        self.limpar_campos()  # Limpa os campos ao inicializar a aba
        self.carregar_lojas()  # Carrega as lojas no comboBox_loja
        self.carregar_feiras()  # Carrega as feiras no comboBox_feira

        # Conecta o evento de clique duplo no treeWidget
        self.treeWidget.itemDoubleClicked.connect(
            self.preencher_campos_do_tree)
        # Conecta o evento de clique simples no treeWidget
        self.treeWidget.itemClicked.connect(self.limpar_campos_tree)

        self.volume_id_selecionado = None  # Armazena o ID do volume selecionado

        # Preenche o campo usuario volume
        self.txt_usuarioVolume.setText(self.usuario)

        # Verifica o tipo de usuário e ajusta a visibilidade do botão cancelar envio
        if self.main_window.tipo_usuario != "administrador":
            self.btn_cancelarVolume.setVisible(False)

    def carregar_volumes(self):
        """
        Carrega todos os volumes do banco de dados e exibe no treeWidget,
        ordenando por Orçamento em ordem decrescente.
        """
        self.treeWidget.clear()  # Limpa a treeWidget antes de carregar os dados

        query = "SELECT id, loja, usuario, orcamento, quantidade, feira, data, data_envio FROM volumes ORDER BY orcamento DESC"
        resultados = database.executar_query_retorno(self.conexao, query)

        if resultados:
            for volume in resultados:
                id, loja, usuario, orcamento, quantidade, feira, data, data_envio = volume

                # Formatando as datas para exibição
                data = data.strftime(
                    '%d/%m/%Y') if isinstance(data, date) else ''
                data_envio = data_envio.strftime(
                    '%d/%m/%Y') if data_envio and isinstance(data_envio, date) else ''

                item = QTreeWidgetItem([
                    str(id),  # ID
                    loja,  # Loja
                    usuario,  # Usuario
                    orcamento,  # Orcamento
                    str(quantidade),  # Quantidade
                    feira,  # Feira
                    data,  # Data
                    data_envio  # Data de Envio
                ])
                self.treeWidget.addTopLevelItem(item)
            # Não precisa ordenar aqui, pois a consulta já retorna ordenada.
            # self.treeWidget.sortItems(3, Qt.DescendingOrder)  # Ordena por Orçamento decrescente
        else:
            utils.mostrar_mensagem(
                "Informação", "Nenhum volume encontrado.", QMessageBox.Information)

    def pesquisar_volume(self):
        """
        Busca um volume pelo Orçamento e preenche os campos do formulário.
        """
        orcamento_pesquisa = self.txt_CodigoPesquisavolume.text().strip()

        if not orcamento_pesquisa:
            utils.mostrar_mensagem("Atenção", "Por favor, insira o número do orçamento para pesquisar.",
                                   QMessageBox.Warning)
            return

        query = f"SELECT id, loja, usuario, orcamento, quantidade, feira, data, data_envio FROM volumes WHERE orcamento = '{orcamento_pesquisa}'"
        resultado = database.executar_query_retorno(self.conexao, query)

        if resultado:
            id, loja, usuario, orcamento, quantidade, feira, data, data_envio = resultado[0]

            # Preenche os campos do formulário com os dados do volume
            self.txt_CodigoPesquisavolume.setText(
                str(id))  # Coloca o ID no campo de pesquisa
            self.comboBox_loja.setCurrentText(loja)  # Mostra a loja
            self.txt_usuarioVolume.setText(usuario)  # Mostra o usuario
            self.txt_orcamentoVolume.setText(orcamento)  # Mostra o orçamento
            self.spinBoxVolume.setValue(quantidade)  # Mostra a quantidade
            self.comboBox_feira.setCurrentText(feira)  # Mostra a feira

            # Converte a data para QDate e define no dateEdit_data
            if isinstance(data, date):
                data_qdate = QDate.fromString(
                    data.strftime('%d/%m/%Y'), "dd/MM/yyyy")
                # Verifique se o widget foi encontrado antes de usá-lo
                if self.dateEdit_data:
                    self.dateEdit_data.setDate(data_qdate)
            else:
                # Verifique se o widget foi encontrado antes de usá-lo
                if self.dateEdit_data:
                    self.dateEdit_data.setDate(QDate.currentDate())

            # Define a data de envio, se houver
            if data_envio and isinstance(data_envio, date):
                data_envio_qdate = QDate.fromString(
                    data_envio.strftime('%d/%m/%Y'), "dd/MM/yyyy")
                # Verifique se o widget foi encontrado antes de usá-lo
                if self.dateEdit_data:
                    self.dateEdit_data.setDate(data_envio_qdate)
            else:
                # Verifique se o widget foi encontrado antes de usá-lo
                if self.dateEdit_data:
                    # Limpa a data de envio se for None
                    self.dateEdit_data.setDate(QDate())

        else:
            utils.mostrar_mensagem(
                "Informação", "Volume não encontrado.", QMessageBox.Information)
            self.limpar_campos()  # Limpa campos após pesquisar caso não ache

    def inserir_volume(self):
        """
        Insere um novo volume no banco de dados.
        """
        loja = self.comboBox_loja.currentText().strip()
        usuario = self.txt_usuarioVolume.text().strip()
        orcamento = self.txt_orcamentoVolume.text().strip()
        quantidade = self.spinBoxVolume.value()
        feira = self.comboBox_feira.currentText().strip()

        # Validação e obtenção da data de dateEdit_data
        if self.dateEdit_data:
            data_qdate = self.dateEdit_data.date()
            if data_qdate.isValid():
                data = data_qdate.toString("yyyy-MM-dd")
            else:
                data = None
        else:
            data = None

        # Valida se o campo orcamento está preenchido
        if not orcamento:
            utils.mostrar_mensagem("Atenção", "Por favor, preencha o número do orçamento.",
                                   QMessageBox.Warning)
            return

        query = """
            INSERT INTO volumes (loja, usuario, orcamento, quantidade, feira, data)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (loja, usuario, orcamento,
                   quantidade, feira, data)

        try:
            cursor = self.conexao.cursor()
            cursor.execute(query, valores)
            self.conexao.commit()
            utils.mostrar_mensagem(
                "Sucesso", "Volume inserido com sucesso!", QMessageBox.Information)
            self.limpar_campos()
            self.carregar_volumes()  # Recarrega a lista de volumes
        except Exception as e:
            utils.mostrar_mensagem(
                "Erro", f"Erro ao inserir volume: {str(e)}", QMessageBox.Critical)
        finally:
            cursor.close()
        self.carregar_volumes()  # Atualiza a treeWidget

    def atualizar_volume(self):
        """
        Atualiza um volume existente no banco de dados.
        """
        if self.volume_id_selecionado is None:
            utils.mostrar_mensagem(
                "Atenção", "Selecione um volume para atualizar.", QMessageBox.Warning)
            return

        loja = self.comboBox_loja.currentText().strip()
        usuario = self.txt_usuarioVolume.text().strip()
        orcamento = self.txt_orcamentoVolume.text().strip()
        quantidade = self.spinBoxVolume.value()
        feira = self.comboBox_feira.currentText().strip()

        # Inicializa as variáveis data e data_envio com valores padrão
        data = None

        # Validação e obtenção da data de dateEdit_data
        if self.dateEdit_data:
            data_qdate = self.dateEdit_data.date()
            if data_qdate.isValid():
                data = data_qdate.toString("yyyy-MM-dd")

        resposta = QMessageBox.question(self, "Confirmação", "Deseja realmente atualizar este volume?",
                                        QMessageBox.Yes | QMessageBox.No)

        if resposta == QMessageBox.Yes:
            query = """
                UPDATE volumes
                SET loja = %s,
                    usuario = %s,
                    orcamento = %s,
                    quantidade = %s,
                    feira = %s,
                    data = %s
                WHERE id = %s
            """
            valores = (loja, usuario, orcamento, quantidade, feira,
                       data, self.volume_id_selecionado)

            try:
                cursor = self.conexao.cursor()
                cursor.execute(query, valores)
                self.conexao.commit()
                utils.mostrar_mensagem(
                    "Sucesso", "Volume atualizado com sucesso!", QMessageBox.Information)
                self.limpar_campos()
                self.carregar_volumes()  # Recarrega a lista de volumes
            except Exception as e:
                utils.mostrar_mensagem(
                    "Erro", f"Erro ao atualizar volume: {str(e)}", QMessageBox.Critical)
            finally:
                cursor.close()
        self.volume_id_selecionado = None  # Desseleciona após atualizar
        self.carregar_volumes()  # Atualiza a treeWidget

    def apagar_volume(self):
        """
        Apaga um volume do banco de dados.
        """

        if self.volume_id_selecionado is None:
            utils.mostrar_mensagem(
                "Atenção", "Selecione um volume para apagar.", QMessageBox.Warning)
            return

        resposta = QMessageBox.question(
            self, "Confirmação", "Deseja realmente apagar este volume?", QMessageBox.Yes | QMessageBox.No)

        if resposta == QMessageBox.Yes:
            query = f"DELETE FROM volumes WHERE id = {self.volume_id_selecionado}"
            if database.executar_query(self.conexao, query):
                utils.mostrar_mensagem(
                    "Sucesso", "Volume apagado com sucesso!", QMessageBox.Information)
                self.limpar_campos()
                self.carregar_volumes()  # Recarrega a lista de volumes
            else:
                utils.mostrar_mensagem(
                    "Erro", f"Erro ao apagar volume.", QMessageBox.Critical)

        self.volume_id_selecionado = None  # Desseleciona após apagar
        self.carregar_volumes()  # Atualiza a treeWidget

    def imprimir_etiquetas(self):
        """  
        Gera um arquivo ZPL para etiquetas e envia diretamente para a impressora.  
        """
        if self.volume_id_selecionado is None:
            self.mostrar_mensagem(
                "Atenção", "Selecione um volume para imprimir a etiqueta.", QMessageBox.Warning)
            return

        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "SELECT loja, usuario, orcamento, quantidade, feira, data FROM volumes WHERE id = %s",
                (self.volume_id_selecionado,))
            volume = cursor.fetchone()
            cursor.close()

            if not volume:
                self.mostrar_mensagem(
                    "Erro", "Nenhum dado retornado do banco para o volume selecionado.", QMessageBox.Critical)
                logging.error(
                    f"Nenhum dado retornado para volume_id: {self.volume_id_selecionado}")
                return

            loja, usuario, orcamento, quantidade, feira, data = volume

            if not quantidade or quantidade <= 0:
                self.mostrar_mensagem(
                    "Erro", "A quantidade de etiquetas é inválida.", QMessageBox.Critical)
                logging.error(
                    f"Quantidade inválida para volume_id: {self.volume_id_selecionado}, quantidade: {quantidade}")
                return

            try:
                # Criar o arquivo ZPL
                nome_arquivo_zpl = "etiquetas.zpl"  # Variável para o nome do arquivo
                with open(nome_arquivo_zpl, "w") as file:
                    for i in range(quantidade):
                        # Configurar o estilo com base no nome da loja
                        # Fundo preto, texto branco
                        if loja.upper() in ["ATACADO", "MARAU", "PF BRASIL"]:
                            file.write("^XA\n")
                            file.write("^PW860\n^LL440\n^MD15\n^PR3,15\n")
                            file.write(
                                "^FO50,50^A0N,50,50^FR^FDLoja: " + loja + "^FS\n")
                            file.write(
                                "^FO50,150^A0N,50,50^FR^FDQuantidade: " + str(quantidade) + "^FS\n")
                            file.write("^FO50,250^A0N,50,50^FR^FDData: " + (
                                data.strftime('%d/%m/%Y') if isinstance(data, date) else '') + "^FS\n")
                            file.write("^XZ\n")
                        # Fundo branco, texto preto
                        elif loja.upper() in ["SERAFINA", "PF MORON", "CASCA"]:
                            file.write("^XA\n")
                            file.write("^PW860\n^LL440\n^MD15\n^PR3,15\n")
                            file.write(
                                "^FO50,50^A0N,50,50^FDLoja: " + loja + "^FS\n")
                            file.write(
                                "^FO50,150^A0N,50,50^FDQuantidade: " + str(quantidade) + "^FS\n")
                            file.write("^FO50,250^A0N,50,50^FDData: " + (
                                data.strftime('%d/%m/%Y') if isinstance(data, date) else '') + "^FS\n")
                            file.write("^XZ\n")

                logging.info(f"Arquivo ZPL criado: {nome_arquivo_zpl}")

                # Enviar o arquivo ZPL diretamente para a impressora
                # Mantenha o nome da impressora aqui
                nome_impressora = r"\\TERMINAL02\ZDesigner GC420t (EPL)"
                comando = f'COPY /B "{nome_arquivo_zpl}" "{nome_impressora}"'

                try:
                    subprocess.run(comando, shell=True, check=True,
                                   capture_output=True, text=True)  # Captura a saída
                    logging.info(
                        f"Etiquetas enviadas para '{nome_impressora}' com sucesso.")
                    self.mostrar_mensagem(
                        "Sucesso", "Etiquetas enviadas para a impressora!", QMessageBox.Information)

                except subprocess.CalledProcessError as e:
                    logging.error(
                        # Log do erro detalhado
                        f"Erro ao enviar para a impressora: {e.stderr}")
                    self.mostrar_mensagem(
                        "Erro", f"Erro ao enviar para a impressora: {e.stderr}", QMessageBox.Critical)

            except Exception as e:
                logging.exception(
                    "Erro ao criar ou enviar o arquivo etiquetas.zpl:")
                self.mostrar_mensagem(
                    "Erro", f"Erro ao criar ou enviar o arquivo etiquetas.zpl: {str(e)}",
                    QMessageBox.Critical)

        except Exception as e:
            logging.exception("Erro ao buscar informações do banco de dados:")
            self.mostrar_mensagem(
                "Erro", f"Erro ao buscar informações do banco de dados: {str(e)}", QMessageBox.Critical)

    def mostrar_mensagem(self, titulo, mensagem, tipo_mensagem):
        """Função auxiliar para exibir mensagens."""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensagem)
        msg_box.setIcon(tipo_mensagem)
        msg_box.exec_()

    def limpar_campos(self):
        """
        Limpa os campos do formulário.
        """
        widgets = [
            self.txt_CodigoPesquisavolume,
            self.comboBox_loja,
            self.txt_usuarioVolume,
            self.txt_orcamentoVolume,
            self.comboBox_feira
        ]
        for widget in widgets:
            if isinstance(widget, QLineEdit):
                widget.clear()

        if self.dateEdit_data:
            # Define data para atual
            self.dateEdit_data.setDate(QDate.currentDate())
        if self.spinBoxVolume:
            self.spinBoxVolume.setValue(0)
        if self.comboBox_loja:
            # Seleciona o item vazio no comboBox_loja
            self.comboBox_loja.setCurrentIndex(0)
        self.volume_id_selecionado = None  # Desseleciona após limpar
        # Preenche o campo usuario volume
        self.txt_usuarioVolume.setText(self.usuario)

    def limpar_campos_tree(self, item, column):
        """
        Limpa os campos do formulário ao clicar em uma linha no treeWidget.
        """
        self.comboBox_loja.setCurrentIndex(0)
        self.txt_usuarioVolume.clear()
        self.txt_orcamentoVolume.clear()
        self.spinBoxVolume.setValue(0)
        self.comboBox_feira.setCurrentIndex(0)
        self.dateEdit_data.setDate(QDate.currentDate())

    def preencher_campos_do_tree(self, item, column):
        """
        Preenche os campos do formulário com os dados da linha selecionada no treeWidget.
        """
        try:
            self.volume_id_selecionado = int(item.text(0))  # Armazena o ID
            self.txt_CodigoPesquisavolume.setText(item.text(0))  # ID
            self.comboBox_loja.setCurrentText(item.text(1))  # Loja
            self.txt_usuarioVolume.setText(self.usuario)  # Usuário logado
            self.txt_orcamentoVolume.setText(item.text(3))  # Orçamento
            self.spinBoxVolume.setValue(int(item.text(4)))  # Quantidade
            self.comboBox_feira.setCurrentText(item.text(5))  # Feira

            # Formata as datas para QDate
            data_str = item.text(6)
            if data_str:
                data_qdate = QDate.fromString(data_str, "dd/MM/yyyy")
                if self.dateEdit_data:
                    self.dateEdit_data.setDate(data_qdate)  # Data
            else:
                if self.dateEdit_data:
                    # Data atual se não houver
                    self.dateEdit_data.setDate(QDate.currentDate())

            # Limpa e preenche a combobox com novos dados
            if self.comboBox is not None:
                self.comboBox.clear()
                # Substitua pelos dados reais
                self.comboBox.addItems(["Item 1", "Item 2", "Item 3"])

        except Exception as e:
            utils.mostrar_mensagem(
                "Erro", f"Erro ao preencher campos: {str(e)}", QMessageBox.Critical)

    def selecionar_item_tree(self, item, column):
        """
        Armazena o ID do volume selecionado para exclusão ou atualização.
        """
        try:
            self.volume_id_selecionado = int(item.text(0))
        except Exception as e:
            utils.mostrar_mensagem(
                "Erro", f"Erro ao selecionar item: {str(e)}", QMessageBox.Critical)

    def carregar_lojas(self):
        """
        Carrega todas as lojas do banco de dados e preenche o comboBox_loja.
        """
        self.comboBox_loja.clear()  # Limpa o comboBox antes de carregar os dados
        # Adiciona um item vazio para iniciar sem valor
        self.comboBox_loja.addItem("")
        query = "SELECT loja FROM lojas"
        resultados = database.executar_query_retorno(self.conexao, query)

        if resultados:
            for loja in resultados:
                self.comboBox_loja.addItem(loja[0])
        else:
            utils.mostrar_mensagem(
                "Informação", "Nenhuma loja encontrada.", QMessageBox.Information)

    def carregar_feiras(self):
        """
        Carrega todas as feiras do banco de dados e preenche o comboBox_feira.
        """
        self.comboBox_feira.clear()
        self.comboBox_feira.addItem("")
        query = "SELECT nome_feira FROM feira ORDER BY nome_feira ASC"
        resultados = database.executar_query_retorno(self.conexao, query)

        if resultados:
            for feira in resultados:
                self.comboBox_feira.addItem(feira[0])
        else:
            utils.mostrar_mensagem(
                "Informação", "Nenhuma feira encontrada.", QMessageBox.Information)

    def atualizar_data_envio(self):
        """
        Atualiza o campo data_envio do volume selecionado com a data atual.
        """
        if self.volume_id_selecionado is None:
            utils.mostrar_mensagem(
                "Atenção", "Selecione um volume para atualizar a data de envio.", QMessageBox.Warning)
            return

        data_envio = QDate.currentDate().toString("yyyy-MM-dd")

        query = """
            UPDATE volumes
            SET data_envio = %s
            WHERE id = %s
        """
        valores = (data_envio, self.volume_id_selecionado)

        try:
            cursor = self.conexao.cursor()
            cursor.execute(query, valores)
            self.conexao.commit()
            utils.mostrar_mensagem(
                "Sucesso", "Data de envio atualizada com sucesso!", QMessageBox.Information)
            self.carregar_volumes()  # Recarrega a lista de volumes
        except Exception as e:
            utils.mostrar_mensagem(
                "Erro", f"Erro ao atualizar data de envio: {str(e)}", QMessageBox.Critical)
        finally:
            cursor.close()
        self.carregar_volumes()  # Atualiza a treeWidget

    def cancelar_envio(self):
        """
        Cancela a data de envio do volume selecionado.
        """
        if self.volume_id_selecionado is None:
            utils.mostrar_mensagem(
                "Atenção", "Selecione um volume para cancelar a data de envio.", QMessageBox.Warning)
            return

        query = """
            UPDATE volumes
            SET data_envio = NULL
            WHERE id = %s
        """
        valores = (self.volume_id_selecionado,)

        try:
            cursor = self.conexao.cursor()
            cursor.execute(query, valores)
            self.conexao.commit()
            utils.mostrar_mensagem(
                "Sucesso", "Data de envio cancelada com sucesso!", QMessageBox.Information)
            self.carregar_volumes()  # Recarrega a lista de volumes
        except Exception as e:
            utils.mostrar_mensagem(
                "Erro", f"Erro ao cancelar data de envio: {str(e)}", QMessageBox.Critical)
        finally:
            cursor.close()
        self.carregar_volumes()  # Atualiza a treeWidget
