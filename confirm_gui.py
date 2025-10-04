"""
Step 2: Confirm or reject detected reference charts using a simple Tkinter GUI.
"""

import json, os
from tkinter import Tk, Label, Button, PhotoImage
from PIL import Image, ImageTk

def review_detections(detected_json="data/detected_references.json",
                      out_json="data/confirmed_references.json",
                      preview_folder="."):
    with open(detected_json) as f:
        detections = json.load(f)
    confirmed = []

    root = Tk()
    root.title("TrueHue – Confirm References")
    img_label = Label(root)
    img_label.pack()

    photo = None  # ✅ declare this here
    idx = 0

    def show(idx):
        nonlocal photo
        item = detections[idx]
        path = os.path.join(preview_folder, item["filename"])
        img = Image.open(path).resize((800, 600))
        photo = ImageTk.PhotoImage(img)
        img_label.config(image=photo)
        root.title(f"{item['filename']}  ({idx+1}/{len(detections)})")

    def accept():
        confirmed.append(detections[idx])
        next_item()

    def reject():
        next_item()

    def next_item():
        nonlocal idx
        idx += 1
        if idx >= len(detections):
            with open(out_json, "w") as f:
                json.dump(confirmed, f, indent=2)
            print(f"✅ Saved {len(confirmed)} confirmed references → {out_json}")
            root.destroy()
        else:
            show(idx)

    Button(root, text="✅ Accept", command=accept).pack(side="left", padx=20)
    Button(root, text="❌ Reject", command=reject).pack(side="right", padx=20)
    show(idx)
    root.mainloop()
