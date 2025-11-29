import sqlite3
from flask import g
import os

def get_db():
    if 'db' not in g:
        # En producción, usa la URL de la base de datos de Railway
        if 'DATABASE_URL' in os.environ:
            # Para PostgreSQL en producción
            import psycopg2
            g.db = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
        else:
            # SQLite para desarrollo local
            g.db = sqlite3.connect('students.db')
            g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    db = get_db()
    cursor = db.cursor()
    
    # Crear tabla estudiantes
    if 'DATABASE_URL' in os.environ:
        # PostgreSQL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20),
                course VARCHAR(50)
            )
        ''')
    else:
        # SQLite
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                course TEXT
            )
        ''')
    
    db.commit()

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()