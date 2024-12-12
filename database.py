import sqlite3
from datetime import datetime

class Database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("messages.db")
        self.cursor = self.conn.cursor()
        self.connect()

    def connect(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            message TEXT NOT NULL,
            channel TEXT NOT NULL,
            date TEXT NOT NULL
        )
        ''')
        self.conn.commit()
        print("Connected to database")

    def insert_message(self, author, message, channel):
        self.cursor.execute("INSERT INTO messages (author, message, channel, date) VALUES (?, ?, ?, ?)", 
                            (author, message, channel, datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
        self.conn.commit()
        print("Message inserted")

    def get_messages_by_author(self, author):
        self.cursor.execute("SELECT * FROM messages WHERE author = ?", (author,))
        return self.cursor.fetchall()
    
    def close(self):
        if self.conn:
            self.conn.close()
            print("Connection closed")