"""
Module cài đặt thuật toán Full RC4 (N = 256) chuẩn cho dữ liệu kiểu bytes.
"""

def ksa(key: bytes) -> bytearray:
    """
    Thuật toán lập lịch khóa (KSA - Key-Scheduling Algorithm).
    Khởi tạo mảng S và T (gồm 256 phần tử) dựa trên khóa K, sau đó hoán vị S.
    """
    # Kiểm tra điều kiện khóa: rỗng hoặc vượt quá 256 byte thì báo lỗi
    if not key:
        raise ValueError("Lỗi: Khóa không được để trống!")
    if len(key) > 256:
        raise ValueError("Lỗi: Khóa phải có độ dài từ 1 đến 256 byte!")
    
    N = len(key)
    # Khởi tạo mảng trạng thái S từ 0 đến 255 và mảng T lặp lại từ khóa K
    S = bytearray(range(256))
    T = bytearray(key[i % N] for i in range(256))
    
    # Giai đoạn hoán vị mảng S
    j = 0
    for i in range(256):
        j = (j + S[i] + T[i]) % 256
        S[i], S[j] = S[j], S[i]  # Hoán đổi giá trị S[i] và S[j]
        
    return S

def prga(S: bytearray, length: int) -> bytes:
    """
    Thuật toán sinh dòng giả ngẫu nhiên (PRGA - Pseudo-Random Generation Algorithm).
    Tiếp tục hoán vị mảng S và trích xuất từng byte keystream để dùng cho phép XOR.
    """
    i = 0
    j = 0
    S_working = bytearray(S)
    keystream_bytes = bytearray()
    
    # Lặp đủ số lượng byte yêu cầu
    for _ in range(length):
        i = (i + 1) % 256
        j = (j + S_working[i]) % 256
        S_working[i], S_working[j] = S_working[j], S_working[i]  # Hoán đổi S[i] và S[j]
        
        t = (S_working[i] + S_working[j]) % 256
        k = S_working[t]
        keystream_bytes.append(k)
        
    return bytes(keystream_bytes)

def keystream(key: bytes, length: int) -> bytes:
    """
    Sinh dòng khóa (keystream) với độ dài cho trước bắt đầu từ vị trí 0.
    Gọi lần lượt KSA và PRGA để tạo ra chuỗi byte giả ngẫu nhiên.
    """
    S = ksa(key)
    return prga(S, length)

def encrypt(data: bytes, key: bytes) -> bytes:
    """
    Mã hóa dữ liệu kiểu bytes bằng cách XOR từng byte dữ liệu với dòng khóa RC4.
    """
    ks = keystream(key, len(data))
    return bytes(b1 ^ b2 for b1, b2 in zip(data, ks))

def decrypt(data: bytes, key: bytes) -> bytes:
    """
    Giải mã dữ liệu kiểu bytes. 
    Do RC4 có tính đối xứng qua phép toán XOR, hàm giải mã thực hiện y hệt hàm mã hóa.
    """
    return encrypt(data, key)