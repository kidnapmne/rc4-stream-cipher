
# Hàm đọc nội dung file dưới dạng bytes.
def read_file(path):
    # Mở file ở chế độ đọc nhị phân.
    with open(path, "rb") as file:
        # Đọc và trả về toàn bộ dữ liệu.
        return file.read()


# Hàm ghi dữ liệu bytes vào file.
def write_file(path, data):
    # Mở file ở chế độ ghi nhị phân.
    with open(path, "wb") as file:
        # Ghi dữ liệu vào file.
        file.write(data)
