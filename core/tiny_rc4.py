def ksa(key, n=8, trace=False):
    """Giai đoạn khởi tạo và xáo trộn S-box (Key-Scheduling Algorithm - KSA).

    Tham số:
        key (list[int]): Khóa bí mật K gồm các số nguyên 3 bit (ví dụ: [2, 1,
        3]).
        n (int): Kích thước mảng S (mặc định N = 8).
        trace (bool): Bật chế độ in chi tiết từng bước.

    Trả về:
        list[int]: Mảng hoán vị S sau khi đã xáo trộn xong.
    """
    # Bước 1: Khởi tạo mảng S tăng dần từ 0 đến N-1
    # Với N = 8: S = [0, 1, 2, 3, 4, 5, 6, 7]
    s = list(range(n))

    # Bước 2: Tạo mảng T bằng cách lặp lại khóa K theo chu kỳ
    # T[i] = K[i mod len(K)]
    key_len = len(key)
    t = [key[i % key_len] for i in range(n)]

    if trace:
        print("\n" + "=" * 60)
        print("--- GIAI ĐOẠN KHỞI TẠO (KSA) ---")
        print(f"Kích thước N = {n}")
        print(f"Khóa K ban đầu = {key} (độ dài = {key_len})")
        print(f"Mảng S ban đầu  = {s}")
        print(f"Mảng T tạo lập = {t}")
        print("-" * 60)

    # Bước 3: Hoán vị mảng S dựa trên T
    j = 0
    for i in range(n):
        # Lưu lại j cũ và phần tử để in giải thích
        j_old = j

        # Công thức: j = (j + S[i] + T[i]) mod N
        j = (j + s[i] + t[i]) % n

        # Hoán đổi hai phần tử S[i] và S[j]
        s_i_val, s_j_val = s[i], s[j]
        s[i], s[j] = s[j], s[i]

        if trace:
            print(
                f"i = {i} | j_mới = ({j_old} + S[{i}]={s_i_val} + T[{i}]={t[i]}) mod {n} = {j} "
                f"| Swap(S[{i}], S[{j}]) -> S = {s}"
            )

    if trace:
        print(f"\n=> Kết quả mảng S sau KSA: {s}")
        print("=" * 60)

    return s


def prga(s, length, n=8, trace=False):
    """Giai đoạn sinh dòng khóa (Pseudo-Random Generation Algorithm - PRGA).

    Tham số:
        s (list[int]): Mảng hoán vị S thu được từ KSA.
        length (int): Số lượng phần tử dòng khóa cần sinh (bằng độ dài dữ liệu).
        n (int): Kích thước mảng S (mặc định 8).
        trace (bool): Bật in chi tiết từng bước.

    Trả về:
        list[int]: Dòng khóa (keystream) gồm length số nguyên 3 bit.
    """
    # Tạo bản sao của S để không làm ảnh hưởng mảng gốc
    s_box = list(s)

    # Khởi tạo con trỏ i = 0, j = 0
    i = 0
    j = 0
    keystream = []

    if trace:
        print("\n" + "=" * 60)
        print("--- GIAI ĐOẠN SINH DÒNG KHÓA (PRGA) ---")
        print(f"Mảng S đầu vào: {s_box}")
        print("-" * 60)

    # Vòng lặp sinh số
    for step in range(length):
        # Bước 1: Cập nhật i = (i + 1) mod N
        i = (i + 1) % n

        # Bước 2: Cập nhật j = (j + S[i]) mod N
        j = (j + s_box[i]) % n

        # Bước 3: Đổi chỗ S[i] và S[j]
        s_box[i], s_box[j] = s_box[j], s_box[i]

        # Bước 4: Tính chỉ số t = (S[i] + S[j]) mod N
        t = (s_box[i] + s_box[j]) % n

        # Bước 5: Lấy giá trị dòng khóa k = S[t]
        k = s_box[t]
        keystream.append(k)

        if trace:
            # Định dạng nhị phân 3 bit: ví dụ 5 -> '101'
            k_bin = f"{k:03b}"
            print(f"Bước {step}:")
            print(f"  i = (i + 1) mod {n} = {i}")
            print(f"  j = (j + S[{i}]) mod {n} = {j}")
            print(f"  Swap(S[{i}], S[{j}]) -> S = {s_box}")
            print(
                f"  t = (S[{i}] + S[{j}]) mod {n} = ({s_box[i]} + {s_box[j]}) mod {n} = {t}"
            )
            print(f"  => Dòng khóa k = S[{t}] = {k} (nhị phân: {k_bin})")

    if trace:
        print(f"\n=> Dòng khóa thu được: {keystream}")
        print("=" * 60)

    return keystream


def tiny_rc4(data, key, n=8, trace=False):
    """Mã hóa hoặc giải mã bằng thuật toán TinyRC4.

    Do phép XOR có tính đối xứng:
      C = P ^ K_stream
      P = C ^ K_stream

    Tham số:
        data (list[int]): Danh sách các số nguyên 3 bit (Bản rõ P hoặc Bản mã
        C).
        key (list[int]): Khóa bí mật K.
        n (int): Không gian trạng thái (mặc định 8).
        trace (bool): Bật in chi tiết.

    Trả về:
        list[int]: Kết quả sau khi XOR với dòng khóa.
    """
    # 1. Chạy thuật toán KSA để khởi tạo mảng trạng thái S
    s_box = ksa(key, n=n, trace=trace)

    # 2. Chạy PRGA để tạo dòng khóa có độ dài tương ứng dữ liệu
    keystream = prga(s_box, length=len(data), n=n, trace=trace)

    # 3. Thực hiện phép toán XOR dữ liệu với dòng khóa
    result = []
    if trace:
        print("\n" + "=" * 60)
        print("--- THỰC HIỆN PHÉP TOÁN XOR (DỮ LIỆU ^ DÒNG KHÓA) ---")

    for idx, (d_val, k_val) in enumerate(zip(data, keystream)):
        xor_res = d_val ^ k_val
        result.append(xor_res)
        if trace:
            d_bin = f"{d_val:03b}"
            k_bin = f"{k_val:03b}"
            res_bin = f"{xor_res:03b}"
            print(
                f"Ký tự {idx}: Dữ liệu = {d_val} ({d_bin}) ^ Khóa = {k_val} ({k_bin}) -> Kết quả = {xor_res} ({res_bin})"
            )

    if trace:
        print("=" * 60 + "\n")

    return result


if __name__ == "__main__":
    # Chạy thử trực tiếp file này với đúng ví dụ slide:
    # N = 8, K = [2, 1, 3], P = [1, 0, 6] (Từ "BAG" -> [001, 000, 110])
    N_SLIDE = 8
    K_SLIDE = [2, 1, 3]
    P_SLIDE = [1, 0, 6]

    print(">>> CHẠY THỬ VỚI VÍ DỤ SLIDE: P = [1, 0, 6] (BAG) <<<")
    # Mã hóa
    cipher = tiny_rc4(P_SLIDE, K_SLIDE, n=N_SLIDE, trace=True)
    print(f"Bản mã C (thập phân): {cipher}")
    print(
        f"Bản mã C (nhị phân)  : {' '.join(f'{x:03b}' for x in cipher)} (Tương ứng từ 'EBA' trên slide)"
    )

    # Giải mã
    plain = tiny_rc4(cipher, K_SLIDE, n=N_SLIDE, trace=False)
    print(f"\nGiải mã lại bản mã C: {plain} (Khớp bản rõ ban đầu: {plain == P_SLIDE})")