import sqlite3
from logging_config import logger
from utils.gpt.logging_database import logging_database

def runner_query(query, origin):
    try:
        connection = sqlite3.connect("valor.sqlite")
    except Exception as e:
        logger.error(f"Falha ao conectar ao banco de dados: {e}")
    cursor =  connection.cursor()
    try:
        cursor.execute(query)
        logging_database(query,origin)
    except Exception as e:
        logger.warning(f"Falha ao criar tabela users: {e}")
    connection.commit()
    connection.close()

# Tables

users = '''
    CREATE TABLE IF NOT EXISTS users (
        id_valor INTEGER PRIMARY KEY AUTOINCREMENT,
        id_discord TEXT NOT NULL,
        name TEXT NOT NULL,     
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
'''  