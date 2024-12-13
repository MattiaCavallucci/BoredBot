import sqlite3
from datetime import datetime

class Database:
    def __init__(self) -> None:
        try:
            self.conn = sqlite3.connect("messages.db")
            self.cursor = self.conn.cursor()
            self.connect()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def connect(self):
        try:
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
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert_message(self, author, message, channel):
        try:
            self.cursor.execute("INSERT INTO messages (author, message, channel, date) VALUES (?, ?, ?, ?)", 
                                (author, message, channel, datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
            self.conn.commit()
            print("Message inserted")
        except sqlite3.Error as e:
            print(f"Error inserting message: {e}")

    def get_messages_by_author(self, author):
        try:
            self.cursor.execute("SELECT * FROM messages WHERE author = ?", (author,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving messages: {e}")
            return []

    def close(self):
        try:
            if self.conn:
                self.conn.close()
                print("Connection closed")
        except sqlite3.Error as e:
            print(f"Error closing connection: {e}")