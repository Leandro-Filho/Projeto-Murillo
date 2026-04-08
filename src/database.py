# src/database.py
import sqlite3

def get_db_connection():
    """Cria a conexão com o banco e ativa o modo WAL para concorrência."""
    conn = sqlite3.connect('dados.db', timeout=10)
    conn.execute('PRAGMA journal_mode=WAL') # Escrituras vão para log separado (.db-wal)
    conn.execute('PRAGMA busy_timeout=5000') # Espera até 5s se estiver ocupado
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Cria as tabelas se não existirem (executa o schema.sql)."""
    conn = get_db_connection()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def inserir_leitura(temperatura, umidade, pressao=None):
    """Insere uma nova leitura no banco (INSERT)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO leituras (temperatura, umidade, pressao)
        VALUES (?, ?, ?)
    ''', (temperatura, umidade, pressao))
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return novo_id

def listar_leituras(limite=50):
    """Retorna as leituras recentes com paginação básica (SELECT)."""
    conn = get_db_connection()
    # Retornando ordenado pelas mais recentes
    leituras = conn.execute('SELECT * FROM leituras ORDER BY timestamp DESC LIMIT ?', (limite,)).fetchall()
    conn.close()
    # Converte os objetos sqlite3.Row em dicionários para facilitar o uso no Flask
    return [dict(leitura) for leitura in leituras]

def buscar_leitura(id_leitura):
    """Busca uma leitura específica pelo ID (SELECT)."""
    conn = get_db_connection()
    leitura = conn.execute('SELECT * FROM leituras WHERE id = ?', (id_leitura,)).fetchone()
    conn.close()
    return dict(leitura) if leitura else None

def atualizar_leitura(id_leitura, dados):
    """Atualiza campos de uma leitura (UPDATE)."""
    conn = get_db_connection()
    # Monta a query dinamicamente de acordo com o que foi enviado no dicionário 'dados'
    campos = []
    valores = []
    for chave, valor in dados.items():
        campos.append(f"{chave} = ?")
        valores.append(valor)
    valores.append(id_leitura)
    
    query = f"UPDATE leituras SET {', '.join(campos)} WHERE id = ?"
    conn.execute(query, valores)
    conn.commit()
    conn.close()

def deletar_leitura(id_leitura):
    """Remove uma leitura do banco (DELETE)."""
    conn = get_db_connection()
    conn.execute('DELETE FROM leituras WHERE id = ?', (id_leitura,))
    conn.commit()
    conn.close()