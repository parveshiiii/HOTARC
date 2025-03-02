import threading
import time
import sqlite3
import os
import json
from cryptography.fernet import Fernet

class MemorySystem:
    def __init__(self, db_file="M1_memory.db", encryption_key=None):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.lock = threading.Lock()
        self.stop_thread = False

        if encryption_key:
            self.fernet = Fernet(encryption_key)
        else:
            self.fernet = Fernet(Fernet.generate_key())

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE,
                value BLOB
            )
        ''')
        self.conn.commit()

    def store_long_term(self, key, value):
        encrypted_value = self.fernet.encrypt(json.dumps(value).encode('utf-8'))
        with self.lock:
            self.cursor.execute('''
                INSERT OR REPLACE INTO memory (key, value)
                VALUES (?, ?)
            ''', (key, encrypted_value))
            self.conn.commit()

    def recall_long_term(self, key):
        with self.lock:
            self.cursor.execute('''
                SELECT value FROM memory WHERE key = ?
            ''', (key,))
            result = self.cursor.fetchone()
            if result:
                encrypted_value = result[0]
                decrypted_value = self.fernet.decrypt(encrypted_value).decode('utf-8')
                return json.loads(decrypted_value)
            else:
                return None

    def store_short_term(self, key, value):
        self.short_term_memory[key] = value

    def recall_short_term(self, key):
        return self.short_term_memory.get(key, None)

    def background_save(self, interval=60):
        def save():
            while not self.stop_thread:
                time.sleep(interval)
                self.conn.commit()
        self.save_thread = threading.Thread(target=save)
        self.save_thread.daemon = True
        self.save_thread.start()

    def stop_background_save(self):
        self.stop_thread = True
        if self.save_thread.is_alive():
            self.save_thread.join()

    def neural_memory_retention(self, key, value):
        self.store_long_term(key, value)

    def save_state(self, state_file):
        state = {
            "encryption_key": self.fernet._signing_key + self.fernet._encryption_key,
        }
        with open(state_file, 'wb') as file:
            pickle.dump(state, file)

    def load_state(self, state_file):
        with open(state_file, 'rb') as file:
            state = pickle.load(file)
        self.fernet = Fernet(state["encryption_key"])