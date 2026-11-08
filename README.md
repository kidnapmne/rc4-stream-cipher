# RC4 Stream Cipher

Bài tập nhóm 6, môn **An toàn và bảo mật thông tin**: cài đặt hệ mã dòng **RC4** bằng Python (TinyRC4 N = 8 và RC4 đầy đủ N = 256), có giao diện Tkinter.

## Cài đặt

**Yêu cầu:** Python 3.10 trở lên và Tkinter (bản Python tải từ [python.org](https://www.python.org/downloads/) đã kèm sẵn). Không cần cài thêm thư viện nào.

Kiểm tra Python:

```bash
python3 --version      # macOS / Linux
python --version       # Windows (hoặc: py --version)
```

Tải mã nguồn:

```bash
git clone https://github.com/kidnapmne/rc4-stream-cipher.git
cd rc4-stream-cipher
```

## Cách chạy

Chạy các lệnh **từ thư mục gốc của dự án** (thư mục chứa `main.py`). Trên Windows thay `python3` bằng `python` hoặc `py`.

| Việc cần làm | Lệnh |
|---|---|
| Mở menu chính | `python3 main.py` |
| Chạy TinyRC4 với ví dụ trên lớp (có trace) | `python3 core/tiny_rc4.py` |
| Mở giao diện đồ hoạ | `python3 -m ui.app_gui` |
| Chạy toàn bộ kiểm thử | `python3 -m unittest discover tests -v` |
| Đo tốc độ mã hoá | `python3 benchmark.py` |
| Minh hoạ tấn công | `python3 attack_demo.py` |

Menu chính (`python3 main.py`): nhập số rồi nhấn Enter. `1` chạy TinyRC4 có trace, `2` chạy kiểm thử, `3` mở giao diện, `0` thoát.

**Kết quả mong đợi**
- TinyRC4 (K = [2, 1, 3], bản rõ "BAG" = [1, 0, 6]): bản mã `[4, 1, 0]`, giải mã lại ra `[1, 0, 6]`.
- Kiểm thử: cuối cùng in `Ran 12 tests` và `OK`.

**Dùng giao diện**
1. Chọn chế độ chữ (TinyRC4) hoặc chế độ file (RC4 đầy đủ).
2. Nhập khoá (không được để trống, tối đa 256 byte).
3. Chế độ chữ: nhập bản rõ rồi bấm "Mã hóa" / "Giải mã".
4. Chế độ file: bấm "Chọn File...", chọn file (ví dụ `data/sample.png`), bấm "Mã hóa" để tạo file `.enc` cạnh file gốc. Để giải mã, chọn file `.enc` và bấm "Giải mã".

## Lỗi thường gặp

| Thông báo | Cách sửa |
|---|---|
| `command not found: python` (macOS) | Dùng `python3` |
| `'python' is not recognized` (Windows) | Cài lại Python và tick "Add python.exe to PATH", hoặc dùng `py` |
| `can't open file ... main.py` | `cd` vào thư mục `rc4-stream-cipher` rồi chạy lại |
| `ModuleNotFoundError: No module named 'core'` | Chạy từ thư mục gốc, dùng dạng `python3 -m ...` |
| `No module named '_tkinter'` | macOS: `brew install python-tk`, hoặc cài Python từ python.org |