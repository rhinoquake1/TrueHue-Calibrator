"""
TrueHue-Calibrator — Command Line Interface
Run the full pipeline via subcommands:
    python truehue.py detect <folder>
    python truehue.py confirm
    python truehue.py calibrate <raw_folder>
    python truehue.py generate
    python truehue.py update <xmp_file>
    python truehue.py visualise
"""

import argparse
import os
import sys

def run_detect(folder):
    os.system(f"python detect_lowres.py {folder}")

def run_confirm():
    os.system("python confirm_gui.py")

def run_calibrate(folder):
    os.system(f"python calibrate_highres.py {folder}")

def run_generate():
    os.system("python generate_profile.py")

def run_update(xmp):
    os.system(f"python update_xmp.py {xmp} TrueHue Neutral v1 IMG_0001.CR3")

def run_visualise():
    os.system("python visualise_dE.py")

def main():
    parser = argparse.ArgumentParser(
        description="🎨 TrueHue-Calibrator CLI — manage camera color profiling workflow"
    )
    sub = parser.add_subparsers(dest="command")

    # detect
    p_detect = sub.add_parser("detect", help="Detect reference charts in low-res images")
    p_detect.add_argument("folder", help="Path to low-res preview folder")

    # confirm
    sub.add_parser("confirm", help="Review and confirm detections via GUI")

    # calibrate
    p_calib = sub.add_parser("calibrate", help="Extract patch RGBs from RAW files")
    p_calib.add_argument("folder", help="Path to RAW or image folder")

    # generate
    sub.add_parser("generate", help="Generate .ti3 calibration data and optional .dcp")

    # update
    p_update = sub.add_parser("update", help="Embed profile info into .xmp file")
    p_update.add_argument("xmp", help="Path to .xmp file to update")

    # visualise
    sub.add_parser("visualise", help="Show ΔE analysis and LAB comparison")

    args = parser.parse_args()

    if args.command == "detect":
        run_detect(args.folder)
    elif args.command == "confirm":
        run_confirm()
    elif args.command == "calibrate":
        run_calibrate(args.folder)
    elif args.command == "generate":
        run_generate()
    elif args.command == "update":
        run_update(args.xmp)
    elif args.command == "visualise":
        run_visualise()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
