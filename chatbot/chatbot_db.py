import sqlite3
from datetime import datetime

DB_NAME = "chatbot_history.db"

def init_chatbot_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_question TEXT,
        bot_response TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_conversation(user_question, bot_response):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO conversations (user_question, bot_response, timestamp)
    VALUES (?, ?, ?)
    """, (user_question, bot_response, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()
    
def view_conversations():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM conversations")

    rows = cursor.fetchall()

    for row in rows:
        print("\nID:", row[0])
        print("User:", row[1])
        print("Bot:", row[2])
        print("Time:", row[3])

    conn.close()
