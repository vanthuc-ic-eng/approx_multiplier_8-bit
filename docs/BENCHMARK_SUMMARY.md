# Unified Cross-Version Multiplier Benchmark Comparison (AMD Zybo Z-7010 & Nangate 45nm)

| Architecture | Git Tag | Slice LUTs | Logic Levels | FPGA Delay | FPGA Fmax | MRED (%) | MED | WCE | FPGA Dyn Pwr @ 100M | ASIC Area (45nm) | ASIC Cells | ASIC Delay (STA) | ASIC Total Pwr @ 100M | DSP |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline (Ban To Chuc)** | `v0.0.0` | 150 | 10 | 9.814 ns | 101.90 MHz | 0.0000% | 0.00 | 0 | 4.00 mW | 350.32 µm² | 296 | 1.150 ns | 178.00 µW | 0 |
| **LUT-ALM V6** | `v0.1.0` | 76 | 11 | 8.476 ns | 117.98 MHz | 3.0494% | 105.69 | 961 | 2.00 mW | 331.70 µm² | 293 | 1.420 ns | 72.00 µW | 0 |
| **LUT-ALM V7 Standard** | `v0.2.0` | 75 | 14 | 9.328 ns | 107.20 MHz | 3.0027% | 104.25 | 961 | 2.00 mW | 367.61 µm² | 317 | 1.470 ns | 99.20 µW | 0 |
| **LUT-ALM V7 High-Prec** | `v0.2.1` | 79 | 14 | 9.298 ns | 107.55 MHz | 2.8011% | 104.22 | 961 | 2.00 mW | 363.09 µm² | 315 | 1.470 ns | 90.10 µW | 0 |
| **LUT-ALM V8 Extreme PPA**| `v0.3.0` | **73** | **10** | **8.878 ns** | **112.64 MHz** | **3.0494%** | **105.69** | **961** | **2.00 mW** | **331.70 µm²** | **293** | **1.420 ns** | **72.00 µW** | **0** |

## Key Evolution & Multi-Target PPA Sign-Off
1. **FPGA Resource Reduction**: Slice LUTs reduced from 150 (Baseline) down to **73 LUTs** in V8 (-51.3% reduction, saving 77 LUTs on Zybo Z-7010).
2. **Timing & Logic Levels**: V8 retains the exact same **10 logic levels** as Baseline with **8.878 ns** data path delay (+10.5% faster than Baseline) while cutting LUTs in half.
3. **FPGA Dynamic Power**: Reduced from 4.00 mW to **2.00 mW** at 100 MHz (-50.0% reduction).
4. **ASIC Nangate 45nm Area**: Reduced from 350.32 µm² down to **331.70 µm²** (-5.3% chip area).
5. **ASIC Power Consumption (OpenSTA)**: Total power reduced from 178.00 µW down to **72.00 µW** at 100 MHz (**-59.5% power consumption** on 45nm standard cell technology).
6. **Mathematical Quality**: MRED = 3.0494% strictly conforming to the < 3.2% error tolerance requirement.
