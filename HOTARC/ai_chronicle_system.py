import json
import os
import time
import logging
from hashlib import md5

class AIChronicleSystem:
    def __init__(self, file_path='chronicles.json', archive_path='archive/', max_entries=1000):
        self.file_path = file_path
        self.archive_path = archive_path
        self.max_entries = max_entries
        self.chronicles = []
        logging.basicConfig(filename='ai_chronicle_system.log', level=logging.INFO)
        self.load_chronicles()

    def load_chronicles(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    self.chronicles = json.load(file)
            logging.info("Chronicles loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load chronicles: {e}")

    def document_evolution(self, entry):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        self.chronicles.append({"timestamp": timestamp, "entry": entry})
        if len(self.chronicles) > self.max_entries:
            self.archive_old_chronicles()
        self.save_chronicles()

    def archive_old_chronicles(self):
        try:
            if not os.path.exists(self.archive_path):
                os.makedirs(self.archive_path)
            archive_file = os.path.join(self.archive_path, f"chronicles_{int(time.time())}.json")
            with open(archive_file, 'w') as file:
                json.dump(self.chronicles[:self.max_entries // 2], file)
            self.chronicles = self.chronicles[self.max_entries // 2:]
            logging.info(f"Archived old chronicles to {archive_file}")
        except Exception as e:
            logging.error(f"Failed to archive chronicles: {e}")

    def save_chronicles(self):
        try:
            temp_file_path = self.file_path + '.tmp'
            with open(temp_file_path, 'w') as file:
                json.dump(self.chronicles, file)
            if self.verify_file_integrity(temp_file_path):
                os.replace(temp_file_path, self.file_path)
                logging.info(f"Chronicles saved to {self.file_path}")
            else:
                logging.error("File integrity check failed. Chronicles not saved.")
        except Exception as e:
            logging.error(f"Failed to save chronicles to {self.file_path}: {e}")

    def verify_file_integrity(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            original_hash = md5(json.dumps(self.chronicles).encode('utf-8')).hexdigest()
            saved_hash = md5(content.encode('utf-8')).hexdigest()
            return original_hash == saved_hash
        except Exception as e:
            logging.error(f"Error verifying file integrity for {file_path}: {e}")
            return False