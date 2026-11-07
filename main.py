"""Menu chính của chương trình RC4.

Chạy:  python3 main.py

Menu có 3 chức năng:
    1. Chạy TinyRC4 có trace (in từng bước KSA, PRGA, XOR).
    2. Chạy kiểm thử (toàn bộ bài test trong thư mục tests/).
    3. Mở giao diện đồ hoạ (Tkinter).
"""

import os
import sys
import unittest

# Thư mục gốc của dự án (thư mục chứa main.py)
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Ví dụ TinyRC4 trên lớp: N = 8, K = [2, 1, 3], P = "BAG" = [1, 0, 6]
N_SLIDE = 8
K_SLIDE = [2, 1, 3]
P_SLIDE = [1, 0, 6]


def print_menu():
    """In menu lựa chọn ra màn hình."""
    print("\n" + "=" * 50)
    print("          CHƯƠNG TRÌNH RC4 - NHÓM 6")
    print("=" * 50)
    print("  1. Chạy TinyRC4 có trace (in từng bước)")
    print("  2. Chạy kiểm thử")
    print("  3. Mở giao diện")
    print("  0. Thoát")
    print("-" * 50)


def run_tiny_trace():
    """Chạy TinyRC4 với ví dụ trên lớp, in từng bước, rồi giải mã lại."""
    from core.tiny_rc4 import tiny_rc4

    print(f"\n>>> TinyRC4: N = {N_SLIDE}, K = {K_SLIDE}, P = {P_SLIDE} (\"BAG\") <<<")
    cipher = tiny_rc4(P_SLIDE, K_SLIDE, n=N_SLIDE, trace=True)
    print(f"Bản mã C (thập phân): {cipher}")
    print(f"Bản mã C (nhị phân)  : {' '.join(f'{x:03b}' for x in cipher)}")

    plain = tiny_rc4(cipher, K_SLIDE, n=N_SLIDE, trace=False)
    print(f"Giải mã lại bản mã C: {plain} (Khớp bản rõ ban đầu: {plain == P_SLIDE})")


def run_tests():
    """Chạy toàn bộ kiểm thử trong thư mục tests/ (giống unittest discover)."""
    print("\n>>> Chạy kiểm thử: python3 -m unittest discover tests -v <<<\n")
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=os.path.join(ROOT, "tests"), top_level_dir=ROOT
    )
    result = unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(suite)
    if result.wasSuccessful():
        print("\n=> Tất cả kiểm thử đạt.")
    else:
        print("\n=> Có kiểm thử không đạt, xem chi tiết ở trên.")


def run_gui():
    """Mở giao diện Tkinter (đóng cửa sổ để quay lại menu)."""
    try:
        import tkinter as tk
        from ui.app_gui import RC4App
    except ImportError as error:
        print(f"\nKhông mở được giao diện: {error}")
        print("Nếu thiếu Tkinter trên macOS: brew install python-tk")
        return

    print("\n>>> Đang mở giao diện... (đóng cửa sổ để quay lại menu) <<<")
    root = tk.Tk()
    RC4App(root)
    root.mainloop()


ACTIONS = {
    "1": run_tiny_trace,
    "2": run_tests,
    "3": run_gui,
}


def main():
    """Vòng lặp menu: hiện menu, nhận lựa chọn, chạy chức năng tương ứng."""
    while True:
        print_menu()
        try:
            choice = input("Nhập lựa chọn (0-3): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nĐã thoát.")
            break

        if choice == "0":
            print("Đã thoát.")
            break

        action = ACTIONS.get(choice)
        if action is None:
            print("Lựa chọn không hợp lệ, vui lòng nhập 0, 1, 2 hoặc 3.")
            continue

        action()


if __name__ == "__main__":
    main()