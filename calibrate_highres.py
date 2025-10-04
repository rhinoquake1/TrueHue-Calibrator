"""
TrueHue-Calibrator — Step 3: Analyse confirmed reference RAWs and extract patch colour data.
© 2025 Jonny Greenwood — Non-commercial use only.
"""

import os
import json
import numpy as np
import rawpy
import cv2
from tqdm import tqdm

def extract_patch_rgb(raw_path, bbox, grid=(4,6)):
    """Extract average RGB values from a chart region in the RAW preview."""
    # Try RAW first, fallback to normal image
    if raw_path.lower().endswith((".cr2", ".cr3", ".nef", ".arw", ".orf", ".raf", ".dng")):
        try:
            with rawpy.imread(raw_path) as raw:
                rgb = raw.postprocess(use_camera_wb=True, no_auto_bright=True, output_bps=8)
        except Exception as e:
            print(f"⚠️ RAW decode failed for {raw_path}: {e}")
            rgb = None
    else:
        rgb = cv2.imread(raw_path)
        if rgb is None:
            raise ValueError(f"❌ Could not open {raw_path} as image.")
    x, y, w, h = bbox
    crop = rgb[y:y+h, x:x+w]
    patch_h, patch_w = h // grid[0], w // grid[1]
    patches = []
    for r in range(grid[0]):
        for c in range(grid[1]):
            y0, y1 = r*patch_h, (r+1)*patch_h
            x0, x1 = c*patch_w, (c+1)*patch_w
            patch = crop[y0:y1, x0:x1]
            mean_rgb = np.mean(patch.reshape(-1,3), axis=0)
            patches.append(mean_rgb)
    return np.array(patches)

def calibrate_from_confirmed(confirmed_json="data/confirmed_references.json",
                             raw_folder=".",
                             out_npy="data/measured_rgb.npy",
                             out_log="data/calibration_log.json"):
    """Iterate over confirmed references and extract measured RGB patches."""
    if not os.path.exists(confirmed_json):
        raise FileNotFoundError(f"{confirmed_json} not found. Run confirm_gui.py first.")
    with open(confirmed_json) as f:
        refs = json.load(f)
    if not refs:
        raise ValueError("No confirmed references found!")

    os.makedirs("data", exist_ok=True)
    all_patches = []
    log = []

    print(f"🔍 Found {len(refs)} confirmed references")
    for ref in refs:
        print("→", ref["filename"], ref["bbox"])

    for ref in tqdm(refs, desc="Extracting patches"):
        raw_path = os.path.join(raw_folder, ref["filename"].replace(".jpg", ".CR3"))
        if not os.path.exists(raw_path):
            # fallback if only preview exists
            raw_path = os.path.join(raw_folder, ref["filename"])
        bbox = ref["bbox"]
        patches = extract_patch_rgb(raw_path, bbox)
        all_patches.append(patches.tolist())
        log.append({"filename": ref["filename"], "bbox": bbox, "num_patches": len(patches)})

    measured = np.array(all_patches)
    np.save(out_npy, measured)
    with open(out_log,"w") as f:
        json.dump(log, f, indent=2)
    print(f"✅ Saved {len(all_patches)} reference samples → {out_npy}")
    return measured

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python calibrate_highres.py /path/to/raws")
    else:
        calibrate_from_confirmed(raw_folder=sys.argv[1])
