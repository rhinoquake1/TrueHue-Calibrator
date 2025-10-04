# ColorChord
# 🎨 TrueHue
*Scene-Aware Color Calibration Toolkit for Photographers*

TrueHue automatically detects ColorChecker references in your photos, computes per-scene white balance and colour transforms, and updates your Lightroom-ready XMPs or generates DCP camera profiles.

---

## 🚀 Features
- Detect ColorChecker charts from RAW previews  
- Confirm or reject detections via GUI  
- Compute per-scene calibration and apply corrections  
- Export `.dcp` profiles (via `dcamprof`)  
- Sync Lightroom XMPs with correct profile + WB  

---

## 🧠 Workflow
```bash
python detect_lowres.py /path/to/raws
python confirm_gui.py
python calibrate_highres.py --chart charts/colorchecker_classic.json
python generate_profile.py
python update_xmp.py
