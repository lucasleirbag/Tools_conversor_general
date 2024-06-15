import logging
from PIL import Image

def view_metadata(file_path):
    try:
        with Image.open(file_path) as img:
            info = img.info
            logging.info(f"Metadados da imagem {file_path}: {info}")
            return info
    except Exception as e:
        logging.error(f"Erro ao visualizar metadados de {file_path}: {e}")
        raise

def remove_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            # Criar uma nova imagem sem metadados
            data = list(img.getdata())
            img_without_metadata = Image.new(img.mode, img.size)
            img_without_metadata.putdata(data)
            
            # Salvar a imagem sem metadados no mesmo caminho
            img_without_metadata.save(image_path)
        logging.info(f"Metadados removidos: {image_path}")
    except Exception as e:
        logging.error(f"Erro ao remover metadados de {image_path}: {e}")
        raise
