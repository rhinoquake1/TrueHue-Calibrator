"""
TrueHue-Calibrator — Step 4: Generate .ti3 and optional .dcp profile from measured RGBs.
© 2025 Jonny Greenwood — Non-commercial use only.
"""

import os
import json
import numpy as np
from datetime import datetime
import subprocess

def load_chart_definition(chart_path):
    with open(chart_path) as f:
        return json.load(f)

def save_ti3(measured_rgb, chart_reference, out_path, camera_name="TrueHue Calibrator"):
    n = measured_rgb.shape[1]
    ref_lab = np.array(chart_reference["patches_lab"])
    if len(ref_lab) != n:
        raise ValueError(f"Chart patch count mismatch: {n} measured vs {len(ref_lab)} reference")

    rgb = np.clip(measured_rgb[0] / 255.0, 0, 1)  # normalise 0–1

    lines = []
    lines.append("CTI3\n")
    lines.append("DESCRIPTOR\tCamera target data\n")
    lines.append(f"CREATED\t{datetime.now().isoformat()}\n")
    lines.append(f"DEVICE_CLASS\tINPUT\n")
    lines.append(f"DEVICE_MODEL\t{camera_name}\n")
    lines.append("INSTRUMENT_TYPE\tCamera\n")
    lines.append("TARGET_INSTRUMENT_TYPE\tSpectrophotometer\n")
    lines.append("BEGIN_DATA_FORMAT\n")
    lines.append("SAMPLE_ID RGB_R RGB_G RGB_B LAB_L LAB_A LAB_B\n")
    lines.append("END_DATA_FORMAT\n")
    lines.append("BEGIN_DATA\n")

    for i, (rgbv, labv) in enumerate(zip(rgb, ref_lab)):
        L, a, b = labv
        R, G, B = rgbv
        lines.append(f"{i+1}\t{R:.6f}\t{G:.6f}\t{B:.6f}\t{L:.4f}\t{a:.4f}\t{b:.4f}\n")

    lines.append("END_DATA\n")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.writelines(lines)
    print(f"✅ Saved {n} patch measurements → {out_path}")

def run_dcamprof(ti3_path, out_dcp="profiles/truehue_neutral.dcp"):
    """Call dcamprof if installed, to generate .dcp."""
    if not shutil.which("dcamprof"):
        print("⚠️ dcamprof not found — skipping .dcp generation.")
        return
    cmd = ["dcamprof", "make-profile", ti3_path, out_dcp, "--output-encoding=matrix"]
    print("🧮 Running:", " ".join(cmd))
    subprocess.run(cmd, check=False)
    print(f"✅ Generated {out_dcp}")

if __name__ == "__main__":
    import shutil
    measured_path = "data/measured_rgb.npy"
    chart_path = "charts/colorchecker_classic.json"
    out_ti3 = "profiles/truehue_measured.ti3"

    if not os.path.exists(measured_path):
        print(f"❌ {measured_path} not found. Run calibrate_highres.py first.")
        exit(1)
    if not os.path.exists(chart_path):
        print(f"❌ {chart_path} not found. Create a chart JSON with reference LAB values.")
        exit(1)

    measured = np.load(measured_path)
    chart = load_chart_definition(chart_path)
    save_ti3(measured, chart, out_ti3)

    # Uncomment this line if you have dcamprof installed:
    # run_dcamprof(out_ti3)
