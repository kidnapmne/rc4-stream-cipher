import os
import time
from core.full_rc4 import encrypt


def run_benchmark():
    """Đo thời gian mã hóa RC4 với các kích thước 1 KB, 100 KB, 1 MB, 10 MB."""
    key = b"benchmark_secret_key_123"
    sizes = [
        ("1 KB", 1024),
        ("100 KB", 100 * 1024),
        ("1 MB", 1024 * 1024),
        ("10 MB", 10 * 1024 * 1024),
    ]

    print("=" * 60)
    print(f"{'BẢNG ĐO TỐC ĐỘ MÃ HÓA FULL RC4 (BENCHMARK)':^60}")
    print("=" * 60)
    print(f"{'Kích thước dữ liệu':<20} | {'Thời gian chạy (giây)':<22} | {'Tốc độ (MB/s)':<12}")
    print("-" * 60)

    for label, num_bytes in sizes:
        data = os.urandom(num_bytes)

        start_time = time.perf_counter()
        encrypt(data, key)
        elapsed_time = time.perf_counter() - start_time

        size_in_mb = num_bytes / (1024 * 1024)
        speed_mbps = size_in_mb / elapsed_time if elapsed_time > 0 else 0.0

        print(f"{label:<20} | {elapsed_time:<22.6f} | {speed_mbps:<12.2f}")

    print("=" * 60)


if __name__ == "__main__":
    run_benchmark()