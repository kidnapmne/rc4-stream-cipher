"""
Demo nhanh cho mục 3.2.2: chạy thử RC4 đầy đủ (core/full_rc4.py).
Chạy từ thư mục gốc của repo:  python demo_full_rc4.py
"""
from core.full_rc4 import keystream, encrypt, decrypt

khoa = b"Key"
ban_ro = b"Plaintext"
ket_qua_chuan = "BBF316E8D940AF0AD3"   # ví dụ chuẩn: khóa "Key", bản rõ "Plaintext"

print("=== 1. Mã hóa ===")
print("Khóa        :", khoa)
print("Bản rõ      :", ban_ro)
day_so = keystream(khoa, len(ban_ro))
print("Dãy số (hex):", day_so.hex().upper())
ban_ma = encrypt(ban_ro, khoa)
print("Bản mã (hex):", ban_ma.hex().upper())
print("Khớp ví dụ chuẩn?", ban_ma.hex().upper() == ket_qua_chuan)

print()
print("=== 2. Giải mã ===")
ban_ro_lai = decrypt(ban_ma, khoa)
print("Bản rõ khôi phục:", ban_ro_lai)
print("Đúng bản rõ ban đầu?", ban_ro_lai == ban_ro)

print()
print("=== 3. Kiểm tra khóa ===")
for ten, khoa_sai in (("Khóa rỗng", b""), ("Khóa 257 byte", bytes(257))):
    try:
        encrypt(ban_ro, khoa_sai)
    except ValueError as loi:
        print(ten, "->", loi)