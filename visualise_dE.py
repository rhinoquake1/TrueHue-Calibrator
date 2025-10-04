"""
TrueHue-Calibrator — Step 6: Visualise ΔE (color difference) between measured RGBs and reference LABs.
© 2025 Jonny Greenwood — Non-commercial use only.
"""

import numpy as np
import json
import matplotlib.pyplot as plt
from colorspacious import cspace_convert
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

def delta_e(lab1, lab2):
    """Compute simple CIE76 ΔE."""
    return np.linalg.norm(lab1 - lab2, axis=1)

def visualise(measured_path="data/measured_rgb.npy", chart_path="charts/colorchecker_classic.json"):
    # Load measured RGBs and reference LABs
    measured = np.load(measured_path)[0] / 255.0
    with open(chart_path) as f:
        chart = json.load(f)
    ref_lab = np.array(chart["patches_lab"])

    # Convert measured RGB → LAB (approx via sRGB)
    measured_lab = cspace_convert(measured, "sRGB1", "CIELab")

    # Compute ΔE per patch
    dE = delta_e(measured_lab, ref_lab)
    avg, maxE, minE = np.mean(dE), np.max(dE), np.min(dE)
    print(f"📊 ΔE summary: mean={avg:.2f}, max={maxE:.2f}, min={minE:.2f}")

    # Plot ΔE bar chart
    plt.figure(figsize=(10,5))
    plt.bar(range(len(dE)), dE, color="skyblue", edgecolor="gray")
    plt.title(f"TrueHue ΔE per patch (avg={avg:.2f}, max={maxE:.2f})")
    plt.xlabel("Patch Index")
    plt.ylabel("ΔE (CIE76)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Optional 3D LAB plot for colour drift
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(ref_lab[:,1], ref_lab[:,2], ref_lab[:,0], color="gray", label="Reference LAB", alpha=0.7)
    ax.scatter(measured_lab[:,1], measured_lab[:,2], measured_lab[:,0], color="red", label="Measured", alpha=0.7)
    ax.set_xlabel("a* (green ↔ red)")
    ax.set_ylabel("b* (blue ↔ yellow)")
    ax.set_zlabel("L* (lightness)")
    ax.set_title("TrueHue LAB Space Comparison")
    ax.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    visualise()
