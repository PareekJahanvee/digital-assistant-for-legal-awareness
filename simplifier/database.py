import sqlite3
from datetime import datetime

DB_NAME = "documents.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        filename TEXT,
        upload_date TEXT,
        original_text TEXT,
        summary TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_document(title, filename, original_text, summary):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO documents (title, filename, upload_date, original_text, summary)
    VALUES (?, ?, ?, ?, ?)
    """, (title, filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), original_text, summary))

    conn.commit()
    conn.close()


def get_all_documents():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, filename, upload_date FROM documents ORDER BY id DESC")
    docs = cursor.fetchall()

    conn.close()
    return docs


def get_document(doc_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM documents WHERE id=?", (doc_id,))
    doc = cursor.fetchone()

    conn.close()
    return doc


def delete_document(doc_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM documents WHERE id=?", (doc_id,))
    conn.commit()

    conn.close()
