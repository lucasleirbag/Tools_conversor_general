import logging
from cryptography.fernet import Fernet

def encrypt_file(file_path, key):
    """Criptografa um arquivo."""
    try:
        fernet = Fernet(key)
        with open(file_path, 'rb') as file:
            original = file.read()
        encrypted = fernet.encrypt(original)
        with open(file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        logging.info(f"Arquivo criptografado: {file_path}")
    except Exception as e:
        logging.error(f"Erro ao criptografar {file_path}: {e}")
        raise

def decrypt_file(file_path, key):
    """Descriptografa um arquivo."""
    try:
        fernet = Fernet(key)
        with open(file_path, 'rb') as encrypted_file:
            encrypted = encrypted_file.read()
        decrypted = fernet.decrypt(encrypted)
        with open(file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted)
        logging.info(f"Arquivo descriptografado: {file_path}")
    except Exception as e:
        logging.error(f"Erro ao descriptografar {file_path}: {e}")
        raise
