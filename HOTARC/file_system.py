import os
import shutil
import hashlib
import logging

class FileSystem:
    def __init__(self):
        logging.basicConfig(filename='file_system.log', level=logging.INFO)

    def save_file(self, file_path, content):
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            if self._verify_file_integrity(file_path, content):
                logging.info(f"File saved successfully: {file_path}")
            else:
                logging.error(f"File integrity check failed after saving: {file_path}")
        except Exception as e:
            logging.error(f"Error saving file {file_path}: {e}")

    def read_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            logging.info(f"File read successfully: {file_path}")
            return content
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {e}")
            return None

    def delete_file(self, file_path):
        try:
            os.remove(file_path)
            logging.info(f"File deleted successfully: {file_path}")
        except Exception as e:
            logging.error(f"Error deleting file {file_path}: {e}")

    def copy_file(self, src_path, dest_path):
        try:
            shutil.copy(src_path, dest_path)
            if self._verify_file_integrity(dest_path, self.read_file(src_path)):
                logging.info(f"File copied successfully from {src_path} to {dest_path}")
            else:
                logging.error(f"File integrity check failed after copying from {src_path} to {dest_path}")
        except Exception as e:
            logging.error(f"Error copying file from {src_path} to {dest_path}: {e}")

    def _verify_file_integrity(self, file_path, original_content):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            if hashlib.md5(content.encode('utf-8')).hexdigest() == hashlib.md5(original_content.encode('utf-8')).hexdigest():
                return True
            else:
                return False
        except Exception as e:
            logging.error(f"Error verifying file integrity for {file_path}: {e}")
            return False