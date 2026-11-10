# Low-Power Approximate Logarithmic Multiplier Architectures for Edge Computing
**Author:** NGUYEN VAN THUC (Student ID: 24161421)  
**Affiliation:** Ho Chi Minh City University of Technology and Education (HCMUTE)  
**Target FPGA Platform:** Digilent Zybo Z7 (AMD Zynq-7000 `xc7z010clg400-1`)  
**Target ASIC Cell Library:** Nangate 45-nm Open Cell Library (`normal.lib`)  

---

## 1. Abstract & Architectural Overview

Approximate computing represents an effective paradigm for resource-constrained deep neural network accelerators deployed on edge devices. Conventional exact multipliers tend to incur noticeable silicon area and dynamic switching power overheads primarily attributable to deep carry-propagate adder structures. To address these overheads, this repository presents a family of Look-Up Table Approximate Logarithmic Multipliers (LUT-ALM). The design methodology leverages piecewise logarithmic approximation derived from Mitchell's theorem, combined with fine-grained error compensation tailored for 6-input LUT FPGA slices and 45-nm standard-cell ASIC implementations.

Experimental synthesis and post-implementation measurements suggest that the proposed logarithmic structures provide a substantial reduction in logic utilization and dynamic power dissipation, while maintaining acceptable mathematical error bounds across exhaustive evaluations.

---

## 2. Versioning and Repository Branch Structure

The design repository adopts an isolated, flat-structure branching methodology. At each designated branch and release tag:
- The `rtl/` directory contains exclusively the flat RTL source files required for that architectural variant (devoid of extraneous subdirectories).
- The `reports/` directory maintains exclusively the self-contained sign-off metrics (FPGA P&R, static timing analysis, dynamic power estimation, exhaustive 16-bit mathematical accuracy, and 45-nm ASIC synthesis).
- Git serves as the primary configuration switcher: checking out any target tag automatically synchronizes both hardware source code and verification artifacts.

### Branch and Release Hierarchy:
- **Branch `v0` (Tag `v0.0.0`)**: Exact Baseline Multiplier (`TheMultiplier`, array-based exact signed 8-bit multiplier), providing reference baseline figures.
- **Branch `v1` (Tag `v0.1.0`, `v0.1.1`)**: **LUT-ALM V6 Architecture** (76 Slice LUTs, 8.476 ns critical path delay, 2.0 mW FPGA dynamic power, MRED = 3.0494%).
- **Branch `v2` (Tag `v0.2.0`, `v0.2.1`, `v0.2.2`)**: **LUT-ALM V7 Architecture** incorporating calibrated fractional mantissa logic (75–79 Slice LUTs, MRED = 2.8011%).
- **Branch `v3` (Tag `v0.3.0`, `v0.3.1`)**: **LUT-ALM V8 Extreme PPA Architecture** (73 Slice LUTs, 10 logic levels, 2.0 mW FPGA dynamic power, MRED = 3.0494%).
- **Branch `v4` (Tag `v0.4.0`, `v0.4.1`, `v0.4.2`)**: **LUT-ALM V9 Multi-Mode Suite** featuring V9-Ultra Balanced (MODE=0, 58 LUTs, MRED = 3.7660%) and V9-Nano Extreme (MODE=2, 36 Slice LUTs, 0 CARRY4 primitives, 4.93 ns critical path delay).
- **Branch `main`**: Master integration branch incorporating the consolidated verification flows and automated bitstream generation scripts.

---

## 3. Directory Layout

```
mult_8bit/
├── Makefile                    # Unified automation interface (verification, implementation, reporting)
├── rtl/                        # Self-contained Verilog source files for active version
├── reports/                    # Sign-off implementation and verification metrics
├── scripts/                    # Automated EDA tool flow scripts (Vivado, Yosys, OpenSTA, evaluation)
├── constrs/                    # Physical FPGA pinout constraints (zybo_z7.xdc)
├── lib/                        # Nangate 45-nm standard cell timing/power library
└── bitstream/                  # Programmed bitstream output for Digilent Zybo Z7
```

---

## 4. Automation and Execution Protocol

The suite provides a standardized command interface through GNU `make`:

### A. Comprehensive Verification and Synthesis
```bash
make accuracy         # Evaluates exhaustive arithmetic accuracy across 65,536 input vectors
make asic             # Executes Nangate 45-nm synthesis (Yosys) and STA/Power estimation (OpenSTA)
make fpga             # Runs physical Place & Route via AMD Vivado (LUT, register, and timing sign-off)
make all              # Sequentially runs accuracy evaluation, ASIC synthesis, and FPGA implementation
```

### B. Metric Inspection
```bash
make report           # Displays a consolidated summary of primary PPA and accuracy metrics
make report-fpga      # Reports FPGA utilization, logic depth, Fmax, and dynamic power
make report-accuracy  # Reports arithmetic error statistics (MRED, MED, WCE)
make report-asic      # Reports ASIC gate count, cell area, static timing delay, and power
make report-timing    # Analyzes FPGA critical path slack and timing constraints
```

### C. Physical Hardware Deployment (Digilent Zybo Z7)
```bash
make bitstream        # Generates hardware bitstream (mult_8bit.bit) with zero DRC violations
make program          # Flashes bitstream directly to target FPGA board via JTAG
```

### D. Clean Protocol
```bash
make clean            # Removes intermediate compilation outputs, EDA logs, and build artifacts
```

---

## 5. Comparative Evaluation Summary

Exhaustive verification across all 65,536 input pairs and physical EDA implementations indicates the following comparative performance profiles:

| Architecture Variant | Tag | Slice LUTs | Logic Levels | Critical Delay | Dynamic Power | Arithmetic MRED | ASIC Cell Area | ASIC Delay | ASIC Power |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Exact Baseline** | `v0.0.0` | 150 | 10 | 9.814 ns | 4.00 mW | 0.0000% | 350.32 µm² | 1.150 ns | 178.00 µW |
| **LUT-ALM V6** | `v0.1.0` | 76 | 11 | 8.476 ns | 2.00 mW | 3.0494% | 331.70 µm² | 1.420 ns | 72.00 µW |
| **LUT-ALM V7 Standard** | `v0.2.0` | 75 | 14 | 9.328 ns | 2.00 mW | 3.0027% | 367.61 µm² | 1.470 ns | 99.20 µW |
| **LUT-ALM V7 High-Precision**| `v0.2.1` | 79 | 14 | 9.298 ns | 2.00 mW | 2.8011% | 363.09 µm² | 1.470 ns | 90.10 µW |
| **LUT-ALM V8 Extreme PPA** | `v0.3.0` | 73 | 10 | 8.878 ns | 2.00 mW | 3.0494% | 331.70 µm² | 1.420 ns | 72.00 µW |
| **LUT-ALM V9-Ultra Balanced**| `v0.4.0` | 58 | 8 | 7.690 ns | 1.80 mW | 3.7660% | 298.40 µm² | 1.310 ns | 58.40 µW |
| **LUT-ALM V9-Nano Extreme** | `v0.4.2` | **36** | **6** | **4.930 ns** | **1.20 mW** | 9.0302% | **184.20 µm²** | **0.980 ns** | **34.10 µW** |

The measured data imply that relative to the exact array multiplier baseline, the V9-Nano extreme variant may achieve up to a 76% reduction in FPGA Slice LUTs and an approximate 47% decrease in ASIC cell area, while maintaining compatibility with deep learning inference tasks exhibiting inherent noise resilience.
