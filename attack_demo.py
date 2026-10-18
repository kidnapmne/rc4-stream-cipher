
"""
Demo hai điểm yếu của RC4:
1. Tái sử dụng cùng khóa cho hai bản rõ.
2. Chạy RC4 với nhiều khoá ngẫu nhiên và đếm số lần byte thứ hai của dòng khoá bằng 0. Số này cao hơn hẳn mức ngẫu nhiên (khoảng gấp đôi), minh hoạ một điểm yếu đã biết của RC4.

"""
import secrets
from core.full_rc4 import keystream


def xor_bytes(data1, data2):
    """XOR hai dãy byte có cùng độ dài."""
    if len(data1) != len(data2):
        raise ValueError("Hai dãy byte phải có cùng độ dài.")

    return bytes(a ^ b for a, b in zip(data1, data2))


def encrypt_with_rc4(plaintext, key):
    """Mã hóa bản rõ bằng dòng khóa RC4."""
    stream = keystream(key, len(plaintext))
    return xor_bytes(plaintext, stream)


def reuse_keystream_demo():
    """
    Mã hóa hai thông điệp bằng cùng khóa.
    Chứng minh C1 XOR C2 = P1 XOR P2.
    """
    plaintext1 = b"Attack at dawn"
    plaintext2 = b"Attack at dusk"

    # Cố ý dùng cùng một khóa để minh họa rủi ro.
    key = b"SameKeyForTest"

    ciphertext1 = encrypt_with_rc4(plaintext1, key)
    ciphertext2 = encrypt_with_rc4(plaintext2, key)

    xor_ciphertexts = xor_bytes(ciphertext1, ciphertext2)
    xor_plaintexts = xor_bytes(plaintext1, plaintext2)

    print("=== DEMO 1: TÁI SỬ DỤNG DÒNG KHOÁ ===")
    print("Plaintext 1:    ", plaintext1.decode("ascii"))
    print("Plaintext 2:    ", plaintext2.decode("ascii"))
    print("Ciphertext 1:   ", ciphertext1.hex())
    print("Ciphertext 2:   ", ciphertext2.hex())
    print("C1 XOR C2:      ", xor_ciphertexts.hex())
    print("P1 XOR P2:      ", xor_plaintexts.hex())
    print("Hai kết quả bằng nhau:",
          xor_ciphertexts == xor_plaintexts)

    assert xor_ciphertexts == xor_plaintexts
    print("KẾT LUẬN: C1 XOR C2 = P1 XOR P2\n")


def run_bias_demo(trials=20000):
    """
    Thử nhiều khóa ngẫu nhiên và đếm số lần byte thứ hai
    của dòng khóa RC4 bằng 0.
    """
    zero_count = 0

    for _ in range(trials):
        # Mỗi lần thử tạo một khóa ngẫu nhiên độc lập dài 16 byte.
        key = secrets.token_bytes(16)

        # Chỉ lấy hai byte đầu của dòng khóa.
        stream = keystream(key, 2)

        # Byte thứ hai ở vị trí số 1.
        if stream[1] == 0:
            zero_count += 1

    # Nếu byte phân bố đều, xác suất bằng 0 là 1/256.
    expected_uniform = trials / 256

    # Mức tham chiếu thiên lệch byte thứ hai
    # của RC4 xấp xỉ 1/128; (tham khảo)
    expected_bias = trials / 128

    print("=== DEMO 2: THỐNG KÊ BYTE THỨ HAI ===")
    print("Số lần thử:                    ", trials)
    print("Số lần byte thứ hai bằng 0:    ", zero_count)
    print("Giá trị kỳ vọng nếu phân bổ đều:       ",
          round(expected_uniform, 2))
    print("Mức tham chiếu xấp xỉ 1/128:   ",
          round(expected_bias, 2))
    print("Tần suất quan sát:             ",
          f"{zero_count / trials:.5%}")
    print("Xác suất nếu phân bổ đều:      ",
          f"{1 / 256:.5%}")
    print("Tỷ lệ so với kỳ vọng nếu phân bổ đều:      ",
          f"{zero_count / expected_uniform:.2f}x")
    print("RC4 có hiện tượng thiên lệch dòng khóa (keystream bias): byte thứ hai của dòng khóa có xác suất bằng 0 cao gấp khoảng hai lần so với một byte ngẫu nhiên phân bố đều")

def main():
    reuse_keystream_demo()
    run_bias_demo()


if __name__ == "__main__":
    main()
