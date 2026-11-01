# Industrial 8-bit Signed Multiplier Suite: From Baseline to LUT-ALM Extreme PPA
**Author:** NGUYEN VAN THUC (Student ID: 24161421)  
**Target Hardware:** Digilent Zybo Z-7010 (AMD Zynq-7000 `xc7z010clg400-1`)  
**Target ASIC Cell Library:** Nangate 45nm Open Cell Library (`normal.lib`)

---

## 1. Kiến Trúc Dự Án & Quản Lý Phiên Bản Git (Chuẩn Công Nghiệp)

Dự án được quản lý qua hệ thống phân nhánh và gắn thẻ (tag) nghiêm ngặt. Tại mỗi nhánh/tag:
- Thư mục `rtl/` được **làm phẳng hoàn toàn** (không chứa thư mục con), chỉ chứa duy nhất mã nguồn RTL của phiên bản đó.
- Thư mục `reports/` được **làm phẳng hoàn toàn** (không chứa thư mục con), chỉ chứa các file báo cáo của riêng phiên bản đó (gồm FPGA P&R, STA Timing, FPGA Power, Mathematical Accuracy, ASIC Synthesis, ASIC OpenSTA Timing & ASIC Power).
- Git đóng vai trò "bộ chuyển đổi phiên bản": `git checkout <tag>` tự động đồng bộ cả mã nguồn RTL và báo cáo tương ứng.

### Cây Phân Nhánh & Thẻ (Tags):
- **Branch `v0` (Tag `v0.0.0`)**: Chứa **Baseline Multiplier** nguyên bản của Ban Tổ Chức (`TheMultiplier`, `exact_mul_s8`), bố trí trực tiếp trong `rtl/`, không chứa bất kỳ file nào của các bản sau.
- **Branch `v1` (Tag `v0.1.0`, `v0.1.1`)**: Kiến trúc **LUT-ALM V6** (76 LUTs, 8.476 ns, 2.0 mW, MRED = 3.0494%), tách biệt hoàn toàn khỏi baseline.
- **Branch `v2` (Tag `v0.2.0`, `v0.2.1`, `v0.2.2`)**: Kiến trúc **LUT-ALM V7** Standard (75 LUTs) và High-Precision (79 LUTs, MRED = 2.8011%).
- **Branch `v3` (Tag `v0.3.0`, `v0.3.1`)**: Kiến trúc **LUT-ALM V8 Extreme PPA** (73 LUTs, 10 logic levels, 8.878 ns delay, 2.0 mW, MRED = 3.0494%).
- **Branch `main`**: Bản phát hành hoàn thiện mới nhất (V8) kèm ma trận đối sánh toàn diện trong `docs/` và file nạp board bitstream.

---

## 2. Cấu Trúc Thư Mục Dự Án

```
mult_8bit/
├── Makefile                    # Makefile điều phối tự động: make all, make clean, make report, make bitstream, make program
├── rtl/                        # Mã nguồn Verilog phẳng trực tiếp của phiên bản hiện hành (không thư mục con)
├── reports/                    # Báo cáo P&R, Timing, Power, Accuracy, ASIC phẳng trực tiếp (không thư mục con)
├── scripts/                    # Bộ công cụ benchmark (Vivado + Yosys + OpenSTA), build bitstream, và nạp board JTAG
├── constrs/                    # File chân vật lý FPGA Digilent Zybo Z-7010 (zybo_z7.xdc)
├── docs/                       # Thuyết minh giải pháp kiến trúc và bảng đối sánh benchmark tổng hợp
├── lib/                        # Thư viện tế bào chuẩn Nangate 45nm (normal.lib)
└── bitstream/                  # File nhị phân nạp board FPGA (mult_8bit.bit)
```

---

## 3. Hướng Dẫn Sử Dụng Makefile

Hệ thống cung cấp giao diện dòng lệnh đồng nhất và tinh gọn qua `Makefile`:

### A. Chạy Benchmark Tự Động
```bash
make accuracy         # Kiểm tra độ chính xác toàn diện 65,536 cặp số (MRED, MED, WCE)
make asic             # Tổng hợp mạch ASIC Nangate 45nm (Yosys) + Đo định thời & công suất (OpenSTA)
make fpga             # Place & Route vật lý trên Vivado 2024.2 (LUTs, Timing, Power)
make all              # Chạy tuần tự cả 3 quy trình trên cho phiên bản hiện tại
```

### B. Xem Báo Cáo Cô Lập Của Phiên Bản Đang Chọn
```bash
make report           # Xem bảng tổng hợp nhanh toàn bộ chỉ số chính
make report-fpga      # Xem chi tiết tài nguyên FPGA (Slice LUTs, Logic Levels, Fmax, Dynamic Power)
make report-accuracy  # Xem chi tiết sai số số học (MRED, Worst-Case Error)
make report-asic      # Xem chi tiết vi mạch ASIC 45nm (Cells, Area, STA Delay, Total Power)
make report-timing    # Xem phân tích đường định thời tới hạn FPGA (Critical Path Slack)
```

### C. Nạp Phần Cứng Lên Board Digilent Zybo Z-7010
```bash
make bitstream        # Tự động build file mult_8bit.bit (DRC passed, 0 errors, Slack MET)
make program          # 1-Click JTAG flash file bitstream trực tiếp lên board phần cứng
```

### D. Dọn Dẹp Toàn Bộ
```bash
make clean            # Xóa sạch toàn bộ build artifacts, EDA logs, reports và bitstream
```

---

## 4. Bảng Tổng Hợp So Sánh Đột Phá Kiến Trúc (FPGA & ASIC Nangate 45nm)

| Phiên bản | Git Tag | Slice LUTs | Logic Levels | FPGA Delay | FPGA Dyn Pwr | Sai số MRED | ASIC Area | ASIC STA Delay | ASIC Total Pwr |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline (Ban Tổ Chức)** | `v0.0.0` | 150 | 10 | 9.814 ns | 4.00 mW | 0.0000% | 350.32 µm² | 1.150 ns | 178.00 µW |
| **LUT-ALM V6** | `v0.1.0` | 76 | 11 | 8.476 ns | 2.00 mW | 3.0494% | 331.70 µm² | 1.420 ns | 72.00 µW |
| **LUT-ALM V7 Standard** | `v0.2.0` | 75 | 14 | 9.328 ns | 2.00 mW | 3.0027% | 367.61 µm² | 1.470 ns | 99.20 µW |
| **LUT-ALM V7 High-Precision** | `v0.2.1` | 79 | 14 | 9.298 ns | 2.00 mW | 2.8011% | 363.09 µm² | 1.470 ns | 90.10 µW |
| **LUT-ALM V8 Extreme PPA** | `v0.3.0` | **73** | **10** | **8.878 ns** | **2.00 mW** | **3.0494%** | **331.70 µm²** | **1.420 ns** | **72.00 µW** |
