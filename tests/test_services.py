import unittest
from app.services.conversion_service import convert_pdf_to_images, resize_image
from app.services.encryption_service import encrypt_file, decrypt_file
from app.services.metadata_service import view_metadata, remove_metadata
from cryptography.fernet import Fernet
import os

class TestServices(unittest.TestCase):

    def setUp(self):
        self.test_file = "test.pdf"
        self.test_image = "test_image.png"
        self.key = Fernet.generate_key()
        # Create test files if they don't exist
        if not os.path.exists(self.test_file):
            with open(self.test_file, 'wb') as f:
                f.write(b'%PDF-1.4 test file')

    def test_convert_pdf_to_images(self):
        convert_pdf_to_images(".", "png", 1)
        self.assertTrue(os.path.exists("converted_images"))

    def test_encrypt_decrypt_file(self):
        encrypt_file(self.test_file, self.key)
        decrypt_file(self.test_file, self.key)
        self.assertTrue(os.path.exists(self.test_file))

    def test_view_remove_metadata(self):
        remove_metadata(self.test_image)
        info = view_metadata(self.test_image)
        self.assertTrue(info)

if __name__ == '__main__':
    unittest.main()
