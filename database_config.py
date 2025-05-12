import sqlite3
from logging_config import logger
from utils.gpt.logging_database import logging_database

def runner_query(query, origin, values=None):
    try:
        connection = sqlite3.connect("valor.sqlite")
    except Exception as e:
        logger.error(f"Falha ao conectar ao banco de dados: {e}")
    cursor =  connection.cursor()
    try:
        if values == None:
            cursor.execute(query)
        else:
            cursor.execute(query,values)
        logging_database(query,origin)
    except Exception as e:
        logger.warning(f"Falha ao executar query: {e}")
    response = cursor.fetchall()
    connection.commit()
    connection.close()
    return response
# Tables

users = '''
    CREATE TABLE IF NOT EXISTS users (
        id_valor INTEGER PRIMARY KEY AUTOINCREMENT,
        id_discord TEXT NOT NULL,
        name TEXT NOT NULL,
        qtd_perguntar INTEGER,
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
'''  
daily_db = '''
CREATE TABLE IF NOT EXISTS daily (
    id_daily INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    daily_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id_valor)
);
'''