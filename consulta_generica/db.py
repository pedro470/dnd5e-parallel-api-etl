import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def criar_conexao():
    try:
        conn = psycopg2.connect(
            dbname= os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        print('Conexão realizada com sucesso!')
        return conn
    except Exception as e:
        print(f'Erro de conexão: {e}')
        return None
    
def fechar_conexao(conn):
    if conn:
        conn.close()
        print('Conexão encerrada.')

def inserir_monstro(conn, monstro):
    try:
        cursor = conn.cursor()
        comando_sql = """
        INSERT INTO monstros_dnd (nome, tipo, nivel_desafio, hp)
        VALUES (%s, %s, %s, %s)
        """
        dados = (monstro['nome'], monstro['tipo'], monstro['nivel_desafio'], monstro['hp'])
        cursor.execute(comando_sql, dados)
        conn.commit()
        cursor.close()
        print(f'Monstro {monstro["nome"]} inserido com sucesso.')
    except Exception as e:
        print(f'Erro ao inserir monstro {monstro["nome"]}: {e}')

def inserir_varios_monstros(conn, monstros):
    try:
        cursor = conn.cursor()
        comando_sql = """
        INSERT INTO monstros_dnd (nome, tipo, cr, hp)
        VALUES (%s, %s, %s, %s)
        """
        dados = [(monstro['nome'], monstro['tipo'], monstro['nivel_desafio'], monstro['hp']) for monstro in monstros]
        cursor.executemany(comando_sql, dados)
        conn.commit()
        cursor.close()
        print(f'{len(monstros)} monstros inseridos com sucesso.')
    except Exception as e:
        print(f'Erro ao inserir vários monstros: {e}')

def buscar_todos_monstros(conn):
    try:
        cursor = conn.cursor()
        comando_sql = "SELECT * FROM monstros_dnd"
        cursor.execute(comando_sql)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
    except Exception as e:
        print(f'Erro ao buscar monstros: {e}')
        return []