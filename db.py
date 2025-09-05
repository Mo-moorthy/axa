import sqlite3, datetime
from pathlib import Path

class DB:
    def __init__(self, path: Path):
        self.conn = sqlite3.connect(path)
        self.init_db()

    def init_db(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS documents (
                        id INTEGER PRIMARY KEY,
                        filename TEXT,
                        uploaded_at TEXT
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS extractions (
                        id INTEGER PRIMARY KEY,
                        document_id INTEGER,
                        key TEXT,
                        value TEXT,
                        confidence REAL,
                        page INTEGER,
                        pattern TEXT
                    )''')
        self.conn.commit()

    def add_document(self, filename: str):
        c = self.conn.cursor()
        c.execute("INSERT INTO documents(filename, uploaded_at) VALUES(?,?)",
                  (filename, datetime.datetime.utcnow().isoformat()))
        self.conn.commit()
        return c.lastrowid

    def add_extractions(self, doc_id, rows):
        c = self.conn.cursor()
        c.executemany("INSERT INTO extractions(document_id,key,value,confidence,page,pattern) VALUES(?,?,?,?,?,?)",
                      [(doc_id,*r) for r in rows])
        self.conn.commit()
