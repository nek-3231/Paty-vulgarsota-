import sqlite3
import os

DB_PATH = os.path.expanduser("~/.paty_audits.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS audits
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, file TEXT, report TEXT)''')
    conn.commit()
    conn.close()

def save_audit(file_path, report):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO audits (timestamp, file, report) VALUES (datetime('now'), ?, ?)", (file_path, report))
    conn.commit()
    conn.close()
