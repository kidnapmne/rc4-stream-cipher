
"""
Kiểm thử RC4 bằng vector tham chiếu RFC 6229
và ba ví dụ RC4 nổi tiếng.
"""

import unittest
from core.full_rc4 import keystream


class TestRFC6229(unittest.TestCase):

    def test_rfc6229_offset_0(self):
        # Khóa 40 bit, offset 0.
        key = bytes.fromhex("0102030405")
        expected = bytes.fromhex(
            "b2396305f03dc027ccc3524a0a1118a8"
        )

        actual = keystream(key, 16)
        self.assertEqual(actual, expected)

    def test_rfc6229_offset_16(self):
        # Cùng khóa, offset 16.
        key = bytes.fromhex("0102030405")
        expected = bytes.fromhex(
            "6982944f18fc82d589c403a47a0d0919"
        )

        # Sinh 32 byte rồi lấy 16 byte ở offset 16.
        actual = keystream(key, 32)[16:32]
        self.assertEqual(actual, expected)

    def test_rfc6229_128bit_offset_0(self):
            #Khoá 128 bits, offset: 0
            key = bytes.fromhex(
                "0102030405060708090a0b0c0d0e0f10"
            )
            expected = bytes.fromhex(
                "9ac7cc9a609d1ef7b2932899cde41b97"
            )
    
            actual = keystream(key, 16)
            self.assertEqual(actual, expected)

    def test_key_plaintext_example(self):
        # Key = "Key", plaintext = "Plaintext".
        key = b"Key"
        plaintext = b"Plaintext"
        expected = bytes.fromhex("bbf316e8d940af0ad3")

        stream = keystream(key, len(plaintext))
        ciphertext = bytes(
            p ^ k for p, k in zip(plaintext, stream)
        )

        self.assertEqual(ciphertext, expected)


    def test_wiki_pedia_example(self):
        # Key = "Wiki", plaintext = "pedia".
        key = b"Wiki"
        plaintext = b"pedia"
        expected = bytes.fromhex("1021bf0420")

        stream = keystream(key, len(plaintext))
        ciphertext = bytes(
            p ^ k for p, k in zip(plaintext, stream)
        )

        self.assertEqual(ciphertext, expected)

    def test_secret_attack_at_dawn_example(self):
        # Key = "Secret", plaintext = "Attack at dawn".
        key = b"Secret"
        plaintext = b"Attack at dawn"
        expected = bytes.fromhex(
            "45a01f645fc35b383552544b9bf5"
        )

        stream = keystream(key, len(plaintext))
        ciphertext = bytes(
            p ^ k for p, k in zip(plaintext, stream)
        )

        self.assertEqual(ciphertext, expected)


if __name__ == "__main__":
    unittest.main()
