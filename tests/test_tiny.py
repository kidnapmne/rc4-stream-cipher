import unittest
from core.tiny_rc4 import tiny_rc4, ksa, prga


class TestTinyRC4(unittest.TestCase):
    def check_example(self, name, key, plaintext, expected_s, expected_keystream, expected_ciphertext):
        """Kiểm tra KSA, PRGA, mã hóa và giải mã theo một ví dụ tham chiếu."""
        n = 8

        # Kiểm tra kết quả KSA và PRGA với bài giải tham chiếu.
        state = ksa(key, n=n, trace=False)
        self.assertEqual(state, expected_s, f"{name}: mảng S sau KSA không khớp")

        keystream = prga(state, length=len(plaintext), n=n, trace=False)
        self.assertEqual(
            keystream, expected_keystream,
            f"{name}: dòng khóa không khớp"
        )

        # Kiểm tra bản mã theo kết quả tính tay.
        ciphertext = tiny_rc4(plaintext, key, n=n, trace=False)
        self.assertEqual(
            ciphertext, expected_ciphertext,
            f"{name}: bản mã không khớp kết quả tính tay"
        )

        # Kiểm tra giải mã khôi phục đúng bản rõ.
        decrypted = tiny_rc4(ciphertext, key, n=n, trace=False)
        self.assertEqual(
            decrypted, plaintext,
            f"{name}: giải mã không khôi phục bản rõ ban đầu"
        )

    def test_slide_example_bag(self):
        """Ví dụ trên slide: K=[2,1,3], P='BAG'=[1,0,6], C='EBA'=[4,1,0]."""
        self.check_example(
            name="Ví dụ trên slide (BAG)",
            key=[2, 1, 3],
            plaintext=[1, 0, 6],
            expected_s=[6, 0, 7, 1, 2, 3, 5, 4],
            expected_keystream=[5, 1, 6],
            expected_ciphertext=[4, 1, 0],
        )

    def test_hand_calculation_example_cba(self):
        """Ví dụ tính tay mục 2.3: K=[1,2,3], P='CBA'=[2,1,0], C='DCC'=[3,2,2]."""
        self.check_example(
            name="Ví dụ tính tay (CBA)",
            key=[1, 2, 3],
            plaintext=[2, 1, 0],
            expected_s=[2, 0, 1, 3, 7, 5, 6, 4],
            expected_keystream=[1, 3, 2],
            expected_ciphertext=[3, 2, 2],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
