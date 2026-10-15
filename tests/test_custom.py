import os
import unittest
from core.full_rc4 import encrypt, decrypt


class TestFullRC4Custom(unittest.TestCase):
    def test_case_1_hello(self):
        """Ca 1: Kiểm thử với chuỗi 'Hello'."""
        original = "Hello".encode("utf-8")
        key = b"secret_key"

        encrypted = encrypt(original, key)
        decrypted = decrypt(encrypted, key)

        assert decrypted == original

    def test_case_2_vietnamese_and_special_chars(self):
        """Ca 2: Chuỗi tiếng Việt có dấu và ký tự đặc biệt với khóa 1 byte và 256 byte."""
        text = "Xin chào Việt Nam! Hệ mật dòng RC4 @#$%^&*()_+-=[]{}|;':,./<>?"
        original = text.encode("utf-8")

        # Thử với khóa 1 byte
        key_1_byte = b"A"
        encrypted_1 = encrypt(original, key_1_byte)
        decrypted_1 = decrypt(encrypted_1, key_1_byte)
        assert decrypted_1 == original

        # Thử với khóa 256 byte
        key_256_bytes = bytes(range(256))
        encrypted_256 = encrypt(original, key_256_bytes)
        decrypted_256 = decrypt(encrypted_256, key_256_bytes)
        assert decrypted_256 == original

    def test_case_3_random_1kb(self):
        """Ca 3: Kiểm thử với 1 KB dữ liệu ngẫu nhiên tạo bằng os.urandom(1024)."""
        original = os.urandom(1024)
        key = os.urandom(16)

        encrypted = encrypt(original, key)
        decrypted = decrypt(encrypted, key)

        assert decrypted == original

    def test_invalid_keys_raise_error(self):
        """Ca báo lỗi: Khóa rỗng (0 byte) và khóa 257 byte phải báo lỗi ValueError."""
        sample_data = b"Test data"

        # Kiểm tra khóa rỗng
        empty_key = b""
        with self.assertRaises(ValueError):
            encrypt(sample_data, empty_key)
        with self.assertRaises(ValueError):
            decrypt(sample_data, empty_key)

        # Kiểm tra khóa dài 257 byte
        long_key = b"K" * 257
        with self.assertRaises(ValueError):
            encrypt(sample_data, long_key)
        with self.assertRaises(ValueError):
            decrypt(sample_data, long_key)


if __name__ == "__main__":
    unittest.main()