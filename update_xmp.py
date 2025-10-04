"""
Step 5: Update Lightroom .xmp files with new camera profile and reference info.
"""

import xml.etree.ElementTree as ET
import os

def update_xmp(xmp_path, profile_name, reference_file):
    tree = ET.parse(xmp_path)
    root = tree.getroot()

    ns = {"crs": "http://ns.adobe.com/camera-raw-settings/1.0/",
          "jonny": "http://jonnygreenwood/calibration"}

    # update or add CameraProfile
    cp = root.find("crs:CameraProfile", ns)
    if cp is None:
        cp = ET.SubElement(root, "{http://ns.adobe.com/camera-raw-settings/1.0/}CameraProfile")
    cp.text = profile_name

    # custom swatch reference
    sr = root.find("jonny:SwatchRef", ns)
    if sr is None:
        sr = ET.SubElement(root, "{http://jonnygreenwood/calibration}SwatchRef")
    sr.text = reference_file

    tree.write(xmp_path, encoding="utf-8", xml_declaration=True)
    print(f"✅ Updated {xmp_path} → {profile_name}")

if __name__=="__main__":
    update_xmp("example.xmp","TrueHue Neutral v1","IMG_0001.CR3")
