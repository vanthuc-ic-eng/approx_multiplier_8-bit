# ==============================================================================
# UNIVERSAL FPGA PHYSICAL IMPLEMENTATION & TIMING BENCHMARK (AMD Vivado 2024.2)
# Target Part: Digilent Zybo Z-7010 (xc7z010clg400-1)
# Author: NGUYEN VAN THUC - 24161421
# ==============================================================================

set_param general.maxThreads 2

if {[info exists env(TOP_MODULE)]} {
    set top_module $env(TOP_MODULE)
} else {
    set top_module "exact_mul_s8_registered"
}

if {[info exists env(DESIGN_NAME)]} {
    set design_name $env(DESIGN_NAME)
} else {
    set design_name "baseline"
}

if {[info exists env(MODE_VAL)]} {
    set mode_val $env(MODE_VAL)
} else {
    set mode_val 2
}

if {[info exists env(TRUNC_BITS)]} {
    set trunc_bits $env(TRUNC_BITS)
} else {
    set trunc_bits 4
}

if {[info exists env(QUAD_CURV)]} {
    set quad_curv $env(QUAD_CURV)
} else {
    set quad_curv 0
}

if {[info exists env(USE_CARRY)]} {
    set use_carry $env(USE_CARRY)
} else {
    set use_carry 1
}

if {[info exists env(REPORT_DIR)]} {
    set report_dir $env(REPORT_DIR)
} else {
    set report_dir "reports"
}

file mkdir $report_dir

puts "\n=================================================================="
puts ">>> PROFILING FPGA: $design_name ($top_module)"
puts ">>> Parameters: TRUNC=$trunc_bits | QUAD=$quad_curv | USE_CARRY=$use_carry"
puts ">>> Output Dir: $report_dir"
puts "=================================================================="

create_project -in_memory -part xc7z010clg400-1

# Read all RTL files present directly in rtl/
set rtl_files [glob -nocomplain rtl/*.v]
read_verilog $rtl_files

# 1. Synthesis (Out-of-context, DSP strictly prohibited)
if {$top_module eq "exact_mul_s8_registered"} {
    synth_design -top $top_module -part xc7z010clg400-1 -mode out_of_context -max_dsp 0
} else {
    synth_design -top $top_module -part xc7z010clg400-1 -mode out_of_context -max_dsp 0 \
        -generic MODE=$mode_val -generic TRUNC_BITS=$trunc_bits -generic QUAD_CURV=$quad_curv -generic USE_CARRY=$use_carry
}

# 2. Place & Route (Physical Implementation for exact sign-off parasitics)
create_clock -period 10.000 [get_ports clk]
opt_design
place_design
route_design

# 3. Post-Route Utilization & Baseline Timing (100 MHz)
report_utilization -file "${report_dir}/pnr_util.rpt"
report_timing_summary -file "${report_dir}/pnr_timing_100mhz.rpt"
report_timing -nworst 1 -max_paths 1 -file "${report_dir}/critical_path.rpt"
report_power -file "${report_dir}/pnr_power_100mhz.rpt"

# 4. Multi-frequency Power & Timing Survey
if {$top_module eq "exact_mul_s8_registered"} {
    set freqs {50 70}
} else {
    set freqs {50 100 105 110}
}

foreach f $freqs {
    set period [expr {1000.0 / $f}]
    create_clock -period $period [get_ports clk]
    report_timing_summary -file "${report_dir}/timing_${f}mhz.rpt"
    report_power -file "${report_dir}/power_${f}mhz.rpt"
}

close_project
puts "\n>>> FPGA Physical Implementation & Timing Benchmark Completed: ${design_name}"
exit
