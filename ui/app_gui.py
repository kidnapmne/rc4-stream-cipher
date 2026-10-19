import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path

# Import các hàm đọc/ghi file từ utils
from utils.file_io import read_file, write_file

# Import thuật toán TinyRC4 từ core/tiny_rc4.py
try:
    from core.tiny_rc4 import tiny_rc4
except ImportError:
    tiny_rc4 = None

# Import thuật toán Full RC4 từ core/full_rc4.py với nhiều tên gọi phổ biến
full_rc4_func = None
try:
    import core.full_rc4 as full_rc4_module
    # Tìm hàm mã hóa phù hợp trong module full_rc4
    for func_name in ['rc4_encrypt', 'rc4', 'full_rc4', 'encrypt', 'rc4_cipher']:
        if hasattr(full_rc4_module, func_name):
            full_rc4_func = getattr(full_rc4_module, func_name)
            break
except Exception as e:
    pass

class RC4App:
    def __init__(self, root):
        self.root = root
        self.root.title("RC4 - Công cụ mã hóa và giải mã")
        self.root.geometry("750x650")
        
        self.mode_var = tk.IntVar(value=1)
        self.file_path = tk.StringVar()

        self.create_widgets()
        self.log("Chương trình đã khởi động.")
        self.log("Đang ở chế độ chữ (TinyRC4).")

    def create_widgets(self):
        # --- Khung nhập khóa ---
        frame_key = tk.LabelFrame(self.root, text=" Nhập khóa: ", padx=10, pady=10)
        frame_key.pack(fill="x", padx=10, pady=10)

        self.key_entry = tk.Entry(frame_key, show="*", width=50, font=("Arial", 11))
        self.key_entry.pack(side="left", padx=5, expand=True, fill="x")
        
        self.show_key_btn = tk.Button(frame_key, text="Hiện", command=self.toggle_key_visibility)
        self.show_key_btn.pack(side="left", padx=5)

        # --- Khung chọn chế độ ---
        frame_mode = tk.LabelFrame(self.root, text=" Chế độ sử dụng: ", padx=10, pady=5)
        frame_mode.pack(fill="x", padx=10, pady=5)

        tk.Radiobutton(
            frame_mode, text="Chế độ chữ (TinyRC4 - TV1)", variable=self.mode_var, value=1, command=self.switch_mode
        ).pack(side="left", padx=20)
        tk.Radiobutton(
            frame_mode, text="Chế độ file (Full RC4 - TV2)", variable=self.mode_var, value=2, command=self.switch_mode
        ).pack(side="left", padx=20)

        # --- Khung nội dung thay đổi theo chế độ ---
        self.frame_content = tk.Frame(self.root)
        self.frame_content.pack(fill="both", expand=True, padx=10, pady=5)

        self.init_text_mode_ui()

        # --- Nhật ký hoạt động ---
        frame_log = tk.LabelFrame(self.root, text=" Nhật ký hoạt động: ", padx=10, pady=5)
        frame_log.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = tk.Text(frame_log, height=8, wrap="word", font=("Consolas", 9))
        self.log_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(frame_log, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

    def log(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")

    def toggle_key_visibility(self):
        if self.key_entry['show'] == '*':
            self.key_entry.config(show='')
            self.show_key_btn.config(text='Ẩn')
        else:
            self.key_entry.config(show='*')
            self.show_key_btn.config(text='Hiện')

    def get_key_bytes(self):
        key_str = self.key_entry.get().strip()
        if not key_str:
            messagebox.showerror("Lỗi", "Bạn chưa nhập khóa!")
            return None
        
        key_bytes = key_str.encode('utf-8')
        if len(key_bytes) > 256:
            messagebox.showwarning("Cảnh báo", "Khóa vượt quá 256 byte! Sẽ bị cắt gọn.")
            key_bytes = key_bytes[:256]
        return key_bytes

    def switch_mode(self):
        for widget in self.frame_content.winfo_children():
            widget.destroy()

        if self.mode_var.get() == 1:
            self.init_text_mode_ui()
            self.log("Đã chuyển sang: Chế độ chữ (TinyRC4)")
        else:
            self.init_file_mode_ui()
            self.log("Đã chuyển sang: Chế độ file (Full RC4)")

    def init_text_mode_ui(self):
        lbl = tk.Label(self.frame_content, text="Văn bản đầu vào hoặc chuỗi HEX:")
        lbl.pack(anchor="w", pady=2)

        self.text_input = tk.Text(self.frame_content, height=6, wrap="word")
        self.text_input.pack(fill="both", expand=True, pady=2)

        btn_frame = tk.Frame(self.frame_content)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Mã hóa → HEX", bg="#e1f5fe", width=15, command=self.process_text_encrypt).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Giải mã HEX → chữ", bg="#e8f5e9", width=18, command=self.process_text_decrypt).pack(side="left", padx=10)

        lbl_out = tk.Label(self.frame_content, text="Kết quả:")
        lbl_out.pack(anchor="w", pady=2)

        self.text_output = tk.Text(self.frame_content, height=6, wrap="word")
        self.text_output.pack(fill="both", expand=True, pady=2)

    def init_file_mode_ui(self):
        lbl = tk.Label(self.frame_content, text="Chọn file cần xử lý mã hóa / giải mã:", font=("Arial", 10, "bold"))
        lbl.pack(anchor="w", pady=10)

        file_frame = tk.Frame(self.frame_content)
        file_frame.pack(fill="x", pady=5)

        tk.Entry(file_frame, textvariable=self.file_path, width=55, state="readonly", font=("Arial", 10)).pack(side="left", padx=5, expand=True, fill="x")
        tk.Button(file_frame, text="Chọn file...", command=self.browse_file, width=12).pack(side="left", padx=5)

        btn_frame = tk.Frame(self.frame_content)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Mã hóa File (.enc)", bg="#ffebee", width=18, height=2, command=lambda: self.process_file(decrypt=False)).pack(side="left", padx=15)
        tk.Button(btn_frame, text="Giải mã File", bg="#e8f5e9", width=18, height=2, command=lambda: self.process_file(decrypt=True)).pack(side="left", padx=15)

    def browse_file(self):
        path = filedialog.askopenfilename(title="Chọn file cần xử lý")
        if path:
            self.file_path.set(path)
            self.log(f"Đã chọn file: {path}")

    def process_text_encrypt(self):
        key = self.get_key_bytes()
        if not key:
            return
        
        plaintext_bytes = self.text_input.get("1.0", "end-1c").encode('utf-8')
        if not plaintext_bytes:
            messagebox.showerror("Lỗi", "Vui lòng nhập văn bản cần mã hóa!")
            return

        try:
            if tiny_rc4 is None:
                raise ImportError("Chưa kết nối được hàm tiny_rc4 trong core/tiny_rc4.py")

            data_list = list(plaintext_bytes)
            key_list = list(key)
            
            result_list = tiny_rc4(data_list, key_list)
            
            ciphertext_bytes = bytes(result_list)
            hex_result = ciphertext_bytes.hex()
            
            self.text_output.delete("1.0", "end")
            self.text_output.insert("1.0", hex_result)
            self.log("Mã hóa văn bản thành công (TinyRC4).")
        except Exception as e:
            messagebox.showerror("Lỗi thuật toán", str(e))
            self.log(f"Lỗi mã hóa văn bản: {e}")

    def process_text_decrypt(self):
        key = self.get_key_bytes()
        if not key:
            return
        
        hex_input = self.text_input.get("1.0", "end-1c").strip().replace(" ", "")
        if not hex_input:
            messagebox.showerror("Lỗi", "Vui lòng nhập chuỗi HEX cần giải mã!")
            return

        try:
            if tiny_rc4 is None:
                raise ImportError("Chưa kết nối được hàm tiny_rc4 trong core/tiny_rc4.py")

            ciphertext_bytes = bytes.fromhex(hex_input)
            data_list = list(ciphertext_bytes)
            key_list = list(key)
            
            result_list = tiny_rc4(data_list, key_list)
            
            plaintext_bytes = bytes(result_list)
            plaintext = plaintext_bytes.decode('utf-8', errors='replace')
            
            self.text_output.delete("1.0", "end")
            self.text_output.insert("1.0", plaintext)
            self.log("Giải mã văn bản thành công (TinyRC4).")
        except ValueError:
            messagebox.showerror("Lỗi định dạng", "Chuỗi đầu vào không phải là mã HEX hợp lệ!")
            self.log("Lỗi: Chuỗi HEX không hợp lệ.")
        except Exception as e:
            messagebox.showerror("Lỗi thuật toán", str(e))
            self.log(f"Lỗi giải mã văn bản: {e}")

    def process_file(self, decrypt):
        key = self.get_key_bytes()
        if not key:
            return

        if not self.file_path.get():
            messagebox.showerror("Lỗi", "Bạn chưa chọn file để xử lý!")
            return

        source = Path(self.file_path.get())

        try:
            data = read_file(source)
            
            if full_rc4_func is None:
                # Nếu không tự dò được, dùng fallback gọi tiny_rc4 hoặc báo lỗi cấu hình
                if tiny_rc4 is not None:
                    res_list = tiny_rc4(list(data), list(key))
                    result = bytes(res_list)
                else:
                    raise ImportError("Chưa kết nối được hàm trong core/full_rc4.py!")
            else:
                # Thử gọi hàm full_rc4 với (data, key) hoặc (key, data)
                try:
                    result = full_rc4_func(data, key)
                except TypeError:
                    result = full_rc4_func(key, data)

                if isinstance(result, list):
                    result = bytes(result)

            action = "Giải mã file" if decrypt else "Mã hóa file"
            suffix = ".dec" if decrypt else ".enc"

            destination = source.with_name(source.name + suffix)
            counter = 1
            while destination.exists():
                destination = source.with_name(source.name + suffix + f".{counter}")
                counter += 1

            write_file(destination, result)
            self.log(f"{action} thành công! Lưu tại: {destination}")
            messagebox.showinfo("Hoàn tất", f"Đã lưu file kết quả:\n{destination}")

        except Exception as error:
            messagebox.showerror("Lỗi xử lý file", str(error))
            self.log(f"Lỗi xử lý file: {error}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RC4App(root)
    root.mainloop()