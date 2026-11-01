#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Mathematical Accuracy Verification Suite for Signed INT8 Multipliers.
Exhaustively evaluates all 65,536 input combinations [-128, 127] x [-128, 127].
Calculates MRED (%), Mean Error Distance (MED), and Worst-Case Error (WCE).
Author: NGUYEN VAN THUC - 24161421
"""

import sys
import json
import argparse
from pathlib import Path

def eval_multiplier(arch="baseline", low_w=3, trunc_bits=4, quad_curv=0):
    lut_low3 = [1, 3, 4, 4, 6, 6, 7, 7]
    
    def enc(x):
        if x < 0:
            mag = (-x) & 0xFF
            sign = 1
        else:
            mag = x & 0xFF
            sign = 0
        zero = (x == 0)
        if zero or mag == 0:
            return sign, zero, 0
        k = mag.bit_length() - 1
        bits = ((mag << (7 - k)) & 0xFF) & 0x7F
        upper = (bits >> 4) & 7
        addr = (bits >> 1) & 7
        low = lut_low3[addr]
        frac = (upper << 3) | low
        return sign, zero, (k << 6) | frac

    total_ae = 0
    total_re = 0.0
    count_nz = 0
    max_ae = 0
    incorrect = 0
    worst_case = None

    for a in range(-128, 128):
        for b in range(-128, 128):
            exact = a * b
            if arch == "baseline":
                approx = exact
            else:
                sa, za, la = enc(a)
                sb, zb, lb = enc(b)
                
                log_sum = la + lb
                exp = (log_sum >> 6) & 0xF
                frac_s = log_sum & 0x3F
                
                if quad_curv:
                    yh = (frac_s >> 3) & 7
                    q_fold = (yh & 3) ^ ((yh >> 2) * 3)
                    q_corr = q_fold >> 1
                else:
                    q_corr = 0
                    
                mantissa = ((1 << 6) | frac_s) - q_corr
                shifted = (mantissa << exp) >> 6
                approx_mag = shifted & 0xFFFF
                
                sign_prod = sa ^ sb
                zero_prod = za | zb
                
                rem_bits = 16 - trunc_bits
                round_bit = ((approx_mag >> (trunc_bits - 1)) & 1) if trunc_bits > 0 else 0
                raw_trunc = (approx_mag >> trunc_bits) & ((1 << rem_bits) - 1)
                
                eff_sign = sign_prod and not zero_prod
                eff_round = round_bit and not zero_prod
                eff_raw = 0 if zero_prod else raw_trunc
                
                carry_in = (not eff_round) if eff_sign else eff_round
                base = (~eff_raw & ((1 << rem_bits) - 1)) if eff_sign else eff_raw
                signed_mag = (base + carry_in) & ((1 << rem_bits) - 1)
                
                res = signed_mag << trunc_bits
                if res >= 0x8000:
                    res -= 0x10000
                approx = res

            ae = abs(approx - exact)
            total_ae += ae
            if ae != 0:
                incorrect += 1
            if ae > max_ae:
                max_ae = ae
                worst_case = {"a": a, "b": b, "approx": approx, "exact": exact, "ae": ae}
            if exact != 0:
                total_re += ae / abs(exact)
                count_nz += 1

    mred = (total_re / count_nz * 100.0) if count_nz > 0 else 0.0
    med = total_ae / 65536.0
    error_rate = (incorrect / 65536.0) * 100.0

    return {
        "architecture": arch,
        "parameters": {"low_w": low_w, "trunc_bits": trunc_bits, "quad_curv": quad_curv},
        "total_cases": 65536,
        "incorrect_cases": incorrect,
        "error_rate_pct": round(error_rate, 4),
        "MRED_pct": round(mred, 4),
        "MED": round(med, 4),
        "WCE": max_ae,
        "worst_case": worst_case
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Signed INT8 Multiplier Accuracy")
    parser.add_argument("--arch", choices=["baseline", "lutalm"], default="baseline")
    parser.add_argument("--trunc", type=int, default=4)
    parser.add_argument("--quad", type=int, default=0)
    parser.add_argument("--out", type=str, default="")
    args = parser.parse_args()

    res = eval_multiplier(arch=args.arch, low_w=3, trunc_bits=args.trunc, quad_curv=args.quad)
    print(f"\n=======================================================")
    print(f" ACCURACY BENCHMARK RESULT: {args.arch.upper()} (TRUNC={args.trunc}, QUAD={args.quad})")
    print(f"=======================================================")
    print(f" MRED (%): {res['MRED_pct']:.4f}%")
    print(f" MED     : {res['MED']:.2f}")
    print(f" WCE     : {res['WCE']}")
    print(f" Error % : {res['error_rate_pct']:.2f}%")
    print(f"=======================================================\n")

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(res, indent=2))
        print(f"[OK] Saved results to: {out_path}")
