import os
import logging
from pdf2image import convert_from_path
from PIL import Image
from app.core.utils import generate_random_id, loading_animation

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

def resize_image(image_path, max_size_mb):
    """Redimensiona a imagem para que não exceda o tamanho máximo especificado."""
    max_size_bytes = max_size_mb * 1024 * 1024
    try:
        with Image.open(image_path) as img:
            img_format = img.format
            quality = 95  # Começando com qualidade alta
            while os.path.getsize(image_path) > max_size_bytes and quality > 10:
                img.save(image_path, format=img_format, quality=quality)
                quality -= 5
            if os.path.getsize(image_path) > max_size_bytes:
                width, height = img.size
                while os.path.getsize(image_path) > max_size_bytes and width > 100 and height > 100:
                    width = int(width * 0.9)
                    height = int(height * 0.9)
                    img = img.resize((width, height), Image.LANCZOS)
                    img.save(image_path, format=img_format, quality=quality)
        logging.info(f"Imagem redimensionada: {image_path}")
    except Exception as e:
        logging.error(f"Erro ao redimensionar imagem {image_path}: {e}")
        raise

def convert_pdf_to_images(input_folder, output_format, max_size_mb):
    output_format = output_format.lower()  # Certificar que o formato esteja em minúsculas

    if output_format not in ["png", "jpg", "jpeg"]:
        logging.error("Formato de saída inválido. Escolha entre 'png', 'jpg' ou 'jpeg'.")
        raise ValueError("Formato de saída inválido. Escolha entre 'png', 'jpg' ou 'jpeg'.")

    if not os.path.exists(input_folder):
        logging.error(f"A pasta {input_folder} não existe.")
        raise FileNotFoundError(f"A pasta {input_folder} não existe.")

    output_folder = os.path.join(input_folder, "converted_images")
    os.makedirs(output_folder, exist_ok=True)

    pdf_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]
    if not pdf_files:
        logging.info("Nenhum arquivo PDF encontrado na pasta.")
        return

    for filename in pdf_files:
        pdf_path = os.path.join(input_folder, filename)
        try:
            images = convert_from_path(pdf_path)
            base_filename = os.path.splitext(filename)[0]
            for i, image in enumerate(images):
                unique_id = generate_random_id()
                output_file = os.path.join(output_folder, f"{base_filename}_{unique_id}.{output_format}")
                logging.info(f"Salvando imagem: {output_file}")
                image.save(output_file, output_format.upper())
                remove_metadata(output_file)
                resize_image(output_file, max_size_mb)
                logging.info(f"Imagem salva e processada: {output_file}")
        except Exception as e:
            logging.error(f"Erro ao converter {filename}: {e}")
            raise
