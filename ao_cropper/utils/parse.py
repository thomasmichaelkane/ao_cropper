import yaml

from .enums import Eye
from . import logging


def load_config():
    with open('config.yaml') as f:
        return yaml.load(f.read(), Loader=yaml.Loader)


def validate(settings):
    """Validates all settings after config load and any CLI overrides."""
    axial_length(settings["acquisition"]["axial_length"])
    mpp(settings["acquisition"]["mpp"])
    crop_size(settings["units"]["crop_size"])


def eye(arg):
    try:
        return Eye[arg]
    except KeyError:
        raise ValueError(f"'{arg}' is not a valid eye — use OD (right) or OS (left)")


def mpp(arg):
    try:
        arg = float(arg)
    except Exception as e:
        raise ValueError(f"mpp must be a number: {e}")

    if not (0.1 < arg < 2):
        logging.warning("microns per pixel is outside the expected range (0.1–2.0 µm/px)")

    return arg


def axial_length(arg):
    try:
        arg = float(arg)
    except Exception as e:
        raise ValueError(f"axial length must be a number: {e}")

    if not (12 < arg < 40):
        logging.warning("axial length is outside the expected range (12–40 mm)")

    return arg


def crop_size(arg):
    try:
        arg = int(arg)
    except Exception as e:
        raise ValueError(f"crop size must be an integer: {e}")

    if not (10 < arg < 400):
        logging.warning("crop size is outside the expected range (10–400 µm)")

    return arg
