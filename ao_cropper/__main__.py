import argparse
import os
import tkinter as tk

from ao_cropper.gui.cropper import Cropper
from ao_cropper.utils import parse, define_parameters, set_max_pixels


def main():

    SETTINGS = parse.load_config()
    args = parse_args(SETTINGS)

    if args.axial_length is not None:
        SETTINGS["acquisition"]["axial_length"] = args.axial_length
    if args.mpp is not None:
        SETTINGS["acquisition"]["mpp"] = args.mpp

    SETTINGS["locate"] = args.locate

    parse.validate(SETTINGS)

    EYE = parse.eye(args.eye)
    parameters = define_parameters(args.image_path, EYE, SETTINGS)
    set_max_pixels(SETTINGS["units"]["max_image_pixels"])

    root = tk.Tk()
    Cropper(root, args.image_path, parameters, SETTINGS)
    root.mainloop()


def valid_tiff(path):
    if not (path.endswith(".tif") or path.endswith(".tiff")):
        raise argparse.ArgumentTypeError(
            f"'{path}' does not have a TIFF extension (.tif or .tiff)"
        )
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"file not found: '{path}'")
    return path


def parse_args(settings):

    acq = settings["acquisition"]

    parser = argparse.ArgumentParser(
        prog="ao-cropper",
        description="Interactively crop subsections from AOSLO retinal images with auto-scaling.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "image file naming convention:\n"
            "  <ID>_<other_info>_<MODALITY>.tif\n"
            "  e.g. MM_0364_OS_combined_0p3796umpx_split.tif\n\n"
            "all TIFFs in the same folder sharing the same base name are\n"
            "treated as additional modalities and cropped simultaneously."
        ),
    )

    parser.add_argument(
        "image_path",
        type=valid_tiff,
        help="path to the TIFF image file",
    )
    parser.add_argument(
        "eye",
        choices=["OD", "OS"],
        help="eye side: OD (right, oculus dexter) or OS (left, oculus sinister)",
    )
    parser.add_argument(
        "-a", "--axial-length",
        type=float,
        default=None,
        metavar="MM",
        help=f"patient axial length in mm (default: {acq['axial_length']} from config.yaml)",
    )
    parser.add_argument(
        "-m", "--mpp",
        type=float,
        default=None,
        metavar="UM/PX",
        help=f"microns per pixel from image metadata (default: {acq['mpp']} from config.yaml)",
    )
    parser.add_argument(
        "-l", "--locate",
        action="store_true",
        help="save maps only — skips extracting individual crops, useful for reviewing placement before a final run",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
