# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import Error
import sys


def criar_conexao(host_name, user_name, user_password, db_name):
    """
    Cria e retorna uma conexão com o banco de dados MySQL.

    Args:
        host_name (str): O nome do host do banco de dados.
        user_name (str): O nome de usuário do banco de dados.
        user_password (str): A senha do usuário do banco de dados.
        db_name (str): O nome do banco de dados.

    Returns:
        mysql.connector.connection.MySQLConnection: Um objeto de conexão com o banco de dados em caso de sucesso,
                                                     ou None em caso de falha.
    """
    conexao = None
    try:
        conexao = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Conexão com o banco de dados MySQL realizada com sucesso")
    except Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        # Imprime informações detalhadas sobre o erro
        print("Detalhes do erro:")
        print(f"  SQLSTATE: {err.sqlstate}")
        print(f"  Error Code: {err.errno}")
        print(f"  Message: {err.msg}")
        sys.exit()  # Encerra o programa em caso de falha na conexão
    return conexao

def executar_query(conexao, query):
    """
    Executa uma query SQL no banco de dados.

    Args:
        conexao (mysql.connector.connection.MySQLConnection): O objeto de conexão com o banco de dados.
        query (str): A query SQL a ser executada.

    Returns:
        bool: True se a query foi executada com sucesso, False caso contrário.
    """
    cursor = conexao.cursor()
    try:
        cursor.execute(query)
        conexao.commit()
        print("Query executada com sucesso")
        return True
    except Error as err:
        print(f"Erro ao executar a query: {err}")
        # Imprime informações detalhadas sobre o erro
        print("Detalhes do erro:")
        print(f"  SQLSTATE: {err.sqlstate}")
        print(f"  Error Code: {err.errno}")
        print(f"  Message: {err.msg}")
        return False
    finally:
        cursor.close() # Fechar o cursor após a execução

def executar_query_retorno(conexao, query):
    """
    Executa uma query SQL no banco de dados e retorna o resultado.

    Args:
        conexao (mysql.connector.connection.MySQLConnection): O objeto de conexão com o banco de dados.
        query (str): A query SQL a ser executada.

    Returns:
        list: Uma lista de tuplas contendo os resultados da query, ou None em caso de erro.
    """
    cursor = conexao.cursor()
    try:
        cursor.execute(query)
        resultado = cursor.fetchall()
        return resultado
    except Error as err:
        print(f"Erro ao executar a query: {err}")
        return None
    finally:
        cursor.close() # Fechar o cursor após a execução

def fechar_conexao(conexao):
    """
    Fecha a conexão com o banco de dados.

    Args:
        conexao (mysql.connector.connection.MySQLConnection): O objeto de conexão com o banco de dados.
    """
    if conexao:
        conexao.close()
        print("Conexão com o banco de dados MySQL fechada")

# Bloco de teste (remover ou comentar antes de usar no projeto principal)
if __name__ == '__main__':
    # Configurações do banco de dados
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = "1234"
    DB_NAME = "controle_de_volumes"

    # Cria a conexão
    conexao = criar_conexao(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

    if conexao:
        # Exemplo de execução de uma query (criação de tabela)
        query_criar_tabela = """
        CREATE TABLE IF NOT EXISTS teste (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL
        );
        """
        executar_query(conexao, query_criar_tabela)

        # Exemplo de inserção de dados
        query_inserir_dados = """
        INSERT INTO teste (nome) VALUES ('Teste 1');
        """
        executar_query(conexao, query_inserir_dados)

        # Exemplo de consulta de dados
        query_selecionar_dados = "SELECT * FROM teste"
        resultados = executar_query_retorno(conexao, query_selecionar_dados)

        if resultados:
            for linha in resultados:
                print(linha)

        # Fecha a conexão
        fechar_conexao(conexao)
    else:
        print("Não foi possível conectar ao banco de dados.")