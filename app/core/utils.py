import random
import string
import sys
import time

def generate_random_id(length=8):
    """Gera um ID único e aleatório."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def loading_animation():
    """Exibe uma animação de carregamento no terminal."""
    chars = "/—\\|"
    for char in chars:
        sys.stdout.write('\r' + 'Carregando... ' + char)
        time.sleep(0.1)
        sys.stdout.flush()
    sys.stdout.write('\r' + 'Carregado!     \n')
