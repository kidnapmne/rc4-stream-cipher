import unittest
from core.tiny_rc4 import tiny_rc4


class TestTinyRC4(unittest.TestCase):
    def test_class_example(self):
        """Kiểm thử TinyRC4 với bộ số liệu ví dụ trên lớp của TV1."""
        # Số liệu từ slide/ví dụ của TV1: N = 8, K = [2, 5], P = [1, 2, 3, 4]
        n = 8
        key = [2, 5]
        plaintext = [1, 2, 3, 4]

        # Kết quả tính tay tương ứng (dòng khóa k = [7, 0, 4, 3] -> P XOR k = [6, 2, 7, 7])
        expected_ciphertext = [5, 2, 2, 0]

        # 1. Mã hóa và khẳng định bản mã khớp với kết quả tính tay
        ciphertext = tiny_rc4(plaintext, key, n, trace=False)
        assert ciphertext == expected_ciphertext, (
            f"Bản mã {ciphertext} không khớp với kết quả tính tay {expected_ciphertext}"
        )

        # 2. Giải mã và khẳng định ra lại đúng bản rõ ban đầu
        decrypted = tiny_rc4(ciphertext, key, n, trace=False)
        assert decrypted == plaintext, (
            f"Bản giải mã {decrypted} không khớp với bản rõ {plaintext}"
        )


if __name__ == "__main__":
    unittest.main()