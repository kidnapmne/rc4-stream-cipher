"""
Demo mục 4.1.2: mã hóa và giải mã file thật bằng RC4 đầy đủ,
rồi so sánh SHA-256 của file gốc và file đã giải mã.
Chạy từ thư mục gốc của repo:  python demo_file_rc4.py
"""
import hashlib   # chỉ dùng để kiểm tra kết quả, không phải phần lõi của RC4
import os
from core.full_rc4 import encrypt, decrypt

KHOA = "KhoaBiMat2026".encode("utf-8")           # khóa dùng cho demo
DANH_SACH_FILE = ["data/test.txt", "data/sample.png"]


def doc_file(duong_dan):
    """Đọc file ra dạng bytes."""
    with open(duong_dan, "rb") as f:
        return f.read()


def ghi_file(duong_dan, du_lieu):
    """Ghi bytes ra file."""
    with open(duong_dan, "wb") as f:
        f.write(du_lieu)


def sha256(du_lieu):
    """Tính SHA-256 (chuỗi 64 ký tự) của dữ liệu."""
    return hashlib.sha256(du_lieu).hexdigest()


bang = []   # lưu các dòng để in bảng ở cuối

for duong_dan in DANH_SACH_FILE:
    ten, duoi = os.path.splitext(duong_dan)      # ví dụ "data/test" và ".txt"
    file_ma_hoa = duong_dan + ".enc"             # data/test.txt.enc
    file_giai_ma = ten + "_giaima" + duoi        # data/test_giaima.txt

    # 1. Đọc file gốc rồi mã hóa, lưu ra file mới (không ghi đè file gốc)
    goc = doc_file(duong_dan)
    ghi_file(file_ma_hoa, encrypt(goc, KHOA))

    # 2. Đọc file mã hóa rồi giải mã, lưu ra file mới
    ma_hoa = doc_file(file_ma_hoa)
    ghi_file(file_giai_ma, decrypt(ma_hoa, KHOA))
    giai_ma = doc_file(file_giai_ma)

    # 3. Ghi lại kích thước và SHA-256 của cả ba file
    bang.append((duong_dan, len(goc), sha256(goc)))
    bang.append((file_ma_hoa, len(ma_hoa), sha256(ma_hoa)))
    bang.append((file_giai_ma, len(giai_ma), sha256(giai_ma)))

    print(duong_dan, "-> giải mã giống file gốc?", giai_ma == goc)

print()
print("| File | Kích thước (byte) | SHA-256 |")
print("|---|---|---|")
for ten_file, kich_thuoc, ma_bam in bang:
    print(f"| {ten_file} | {kich_thuoc} | {ma_bam} |")