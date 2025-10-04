"""
TrueHue-Calibrator — Step 1: Detect ColorChecker candidates from low-res RAW previews.
© 2025 Jonny Greenwood — Non-commercial use only.
"""

import cv2
import os
import json
import numpy as np
from tqdm import tqdm

def detect_colorcharts(raw_folder, out_json="data/detected_references.json"):
    detections = []
    for file in tqdm(os.listdir(raw_folder)):
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        path = os.path.join(raw_folder, file)
        img = cv2.imread(path)
        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        edges = cv2.Canny(blur, 60, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            ratio = w/h if h != 0 else 0
            area = w*h
            if 0.8 < ratio < 1.2 and 10000 < area < 300000:
                detections.append({"filename": file, "bbox": [int(x), int(y), int(w), int(h)], "score": area})

    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, "w") as f:
        json.dump(detections, f, indent=2)
    print(f"✅ Detected {len(detections)} candidate charts → {out_json}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python detect_lowres.py /path/to/previews")
    else:
        detect_colorcharts(sys.argv[1])
