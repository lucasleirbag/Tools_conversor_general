import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.ui.menu import main_menu

if __name__ == "__main__":
    main_menu()
