import logging
from app.core.logging_config import configure_logging
from app.core.utils import loading_animation
from app.services.conversion_service import convert_pdf_to_images
from app.services.encryption_service import encrypt_file, decrypt_file
from app.services.metadata_service import view_metadata, remove_metadata
from cryptography.fernet import Fernet
import shutil

def main_menu():
    configure_logging()

    while True:
        print("Selecione uma opção:")
        print("1. Converter PDF para Imagem")
        print("2. Criptografar Imagem")
        print("3. Descriptografar Imagem")
        print("4. Ver Metadados da Imagem")
        print("5. Limpar Metadados da Imagem")
        print("6. Sair")

        choice = input("Digite a opção desejada: ").strip()

        if choice == '1':
            input_folder = input("Digite o caminho para a pasta contendo os arquivos PDF: ").strip()
            output_format = input("Digite o formato de saída desejado (png, jpg ou jpeg): ").strip()
            max_size_mb = float(input("Digite o tamanho máximo da imagem em MB: ").strip())

            # Verifique se o Poppler está instalado
            if not shutil.which("pdftoppm"):
                logging.error("Poppler não está instalado ou não está no PATH. Instale o Poppler e adicione ao PATH.")
                continue

            try:
                loading_animation()
                convert_pdf_to_images(input_folder, output_format, max_size_mb)
            except Exception as e:
                logging.error(f"Erro: {e}")
                break

        elif choice == '2':
            file_path = input("Digite o caminho para a imagem que deseja criptografar: ").strip()
            key = Fernet.generate_key()
            logging.info(f"Chave de criptografia gerada: {key.decode()}")

            try:
                loading_animation()
                encrypt_file(file_path, key)
            except Exception as e:
                logging.error(f"Erro: {e}")
                break

        elif choice == '3':
            file_path = input("Digite o caminho para a imagem que deseja descriptografar: ").strip()
            key = input("Digite a chave de criptografia: ").encode()

            try:
                loading_animation()
                decrypt_file(file_path, key)
            except Exception as e:
                logging.error(f"Erro: {e}")
                break

        elif choice == '4':
            file_path = input("Digite o caminho para a imagem que deseja ver os metadados: ").strip()
            try:
                loading_animation()
                info = view_metadata(file_path)
                print(info)
            except Exception as e:
                logging.error(f"Erro ao visualizar metadados de {file_path}: {e}")
                break

        elif choice == '5':
            file_path = input("Digite o caminho para a imagem que deseja limpar os metadados: ").strip()

            try:
                loading_animation()
                remove_metadata(file_path)
            except Exception as e:
                logging.error(f"Erro: {e}")
                break

        elif choice == '6':
            break

        else:
            print("Opção inválida. Tente novamente.")
