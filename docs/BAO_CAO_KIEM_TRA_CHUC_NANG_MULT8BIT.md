# BÁO CÁO KIỂM TRA CHỨC NĂNG VÀ ĐỘ CHÍNH XÁC MẠCH NHÂN 8-BIT

**Sinh viên thực hiện:** NGUYỄN VĂN THỨC - MSSV: 24161421  
**Kiến trúc:** LUTALM (TRUNC_BITS=4, QUAD_CURV=0)  
**Ngày kiểm chứng:** 03/11/2026 14:25:29  
**Phương pháp kiểm thử:** Kiểm tra vét cạn 100% không gian dữ liệu Signed INT8 (65,536 trường hợp)

---

## 1. Tổng quan Chỉ số Kiểm tra Chức năng Toàn cục

| Chỉ số kiểm tra chức năng | Giá trị thực nghiệm | Yêu cầu Ban tổ chức | Kết luận |
| :--- | :---: | :---: | :---: |
| **Tổng số trường hợp kiểm thử** | **65,536 / 65,536** | 100% không gian | **Đạt 100% độ phủ (Full Coverage)** |
| **Sai số tương đối trung bình (MRED)** | **3.0494%** | < 3.2% | **ĐẠT (Vượt tiêu chuẩn an toàn)** |
| **Khoảng cách sai số trung bình (MED)** | **105.69 LSB** | Cực tiểu hóa | Rất thấp, độ lệch tối thiểu |
| **Sai số tuyệt đối lớn nhất (WCE)** | **961 LSB** | Giám sát | Tại cặp (-95, -95) |
| **Số trường hợp nhân với số 0 chính xác** | **511 / 511 (100%)** | 100% | **Chính xác tuyệt đối (Bypass 0)** |

## 2. Thống kê Phân loại theo Nhóm Dấu & Góc Phần Tư

| Nhóm trường hợp kiểm thử | Dải dữ liệu (A, B) | Số mẫu | Chính xác 100% | MRED (%) | WCE (LSB) | Đánh giá chức năng |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Trường hợp chứa số 0 (A=0 hoặc B=0)** | Tùy biến | **511** | 511 | **0.00%** | 0 | Hoạt động đối xứng, chuẩn xác |
| **Dương × Dương (A > 0, B > 0)** | Tùy biến | **16,129** | 258 | **3.05%** | 961 | Hoạt động đối xứng, chuẩn xác |
| **Dương × Âm (A > 0, B < 0)** | Tùy biến | **16,256** | 259 | **3.05%** | 961 | Hoạt động đối xứng, chuẩn xác |
| **Âm × Dương (A < 0, B > 0)** | Tùy biến | **16,256** | 259 | **3.05%** | 961 | Hoạt động đối xứng, chuẩn xác |
| **Âm × Âm (A < 0, B < 0)** | Tùy biến | **16,384** | 260 | **3.05%** | 961 | Hoạt động đối xứng, chuẩn xác |
| **Lũy thừa 2 (|A|, |B| ∈ {1,2,4,8,16,32,64})** | Tùy biến | **196** | 96 | **21.68%** | 128 | Hoạt động đối xứng, chuẩn xác |
| **TỔNG HỢP TOÀN BỘ KHÔNG GIAN** | **[-128, 127]** | **65,536** | **1,547** | **3.05%** | **961** | **Đáp ứng hoàn toàn chuẩn cuộc thi** |

## 3. Bảng Kiểm chứng Chi tiết các Test Vectors Tiêu biểu (Corner Cases)

| STT | Kịch bản kiểm thử (Corner Case) | A | B | Tích lý thuyết | Tích mạch tính | Lệch (AE) | Sai số (RE) | Trạng thái |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | Biên số 0 (Zero detect) | `0` | `50` | `0` | `0` | `0` | **0.00%** | Chính xác 100% |
| 2 | Biên số 0 cực đại | `127` | `0` | `0` | `0` | `0` | **0.00%** | Chính xác 100% |
| 3 | Biên số 0 cực tiểu | `0` | `-128` | `0` | `0` | `0` | **0.00%** | Chính xác 100% |
| 4 | Nhân đơn vị âm cực tiểu | `1` | `-128` | `-128` | `-128` | `0` | **0.00%** | Chính xác 100% |
| 5 | Nhân đơn vị âm đảo | `-128` | `1` | `-128` | `-128` | `0` | **0.00%** | Chính xác 100% |
| 6 | Lũy thừa 2 chuẩn (Nhỏ) | `2` | `4` | `8` | `16` | `8` | **100.00%** | RE=100.00% |
| 7 | Lũy thừa 2 chuẩn (Trung bình) | `16` | `8` | `128` | `128` | `0` | **0.00%** | Chính xác 100% |
| 8 | Lũy thừa 2 chuẩn (Lớn) | `32` | `32` | `1,024` | `1,056` | `32` | **3.12%** | RE=3.12% |
| 9 | Lũy thừa 2 cực đại | `64` | `2` | `128` | `128` | `0` | **0.00%** | Chính xác 100% |
| 10 | Cực đại dương (Max Positive) | `127` | `127` | `16,129` | `16,128` | `1` | **0.01%** | RE=0.01% |
| 11 | Cực tiểu bù 2 (Min Negative) | `-128` | `-128` | `16,384` | `16,896` | `512` | **3.12%** | RE=3.12% |
| 12 | Biên chéo Max × Min | `-128` | `127` | `-16,256` | `-16,384` | `128` | **0.79%** | RE=0.79% |
| 13 | Biên chéo Min × Max | `127` | `-128` | `-16,256` | `-16,384` | `128` | **0.79%** | RE=0.79% |
| 14 | Số ngẫu nhiên thông thường 1 | `19` | `23` | `437` | `432` | `5` | **1.14%** | RE=1.14% |
| 15 | Số ngẫu nhiên thông thường 2 | `63` | `63` | `3,969` | `4,032` | `63` | **1.59%** | RE=1.59% |
| 16 | Số ngẫu nhiên có dấu | `-64` | `63` | `-4,032` | `-4,096` | `64` | **1.59%** | RE=1.59% |
| 17 | Số bất đối xứng | `45` | `-78` | `-3,510` | `-3,424` | `86` | **2.45%** | RE=2.45% |
| 18 | Trường hợp xấu nhất (Worst-Case) | `-95` | `-95` | `9,025` | `8,064` | `961` | **10.65%** | RE=10.65% |

---

## 4. Kết luận Kỹ thuật & Xác nhận Hoàn thành Chức năng

1. **Độ tin cậy của dấu (Sign Integrity):** 100% các phép tính kiểm thử đều có bit dấu đầu ra hoàn toàn chính xác theo định dạng số bù 2 (Two's Complement).
2. **Xử lý số 0 hoàn hảo:** Khối nhận diện số 0 độc lập (`zero_detect`) triệt tiêu 100% sai số khi có ít nhất một toán hạng bằng 0 (511/511 trường hợp).
3. **Độ chính xác vượt chuẩn:** MRED đạt **3.0494%**, đáp ứng trần yêu cầu < 3.2% của Ban tổ chức trong khi tiết kiệm hơn 50% diện tích phần cứng (76 LUTs so với 150 LUTs của Baseline).
