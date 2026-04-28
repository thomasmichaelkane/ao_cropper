import os
from PIL import Image


def set_max_pixels(max_pixels):
    Image.MAX_IMAGE_PIXELS = max_pixels


def conversions(settings):
    acq = settings["acquisition"]
    units = settings["units"]

    crop_size_pix = units["crop_size"] / acq["mpp"]
    microns_per_degree = (acq["axial_length"] / units["model_eye_length"]) * units["reference_mpd"]
    pixels_per_degree = microns_per_degree / acq["mpp"]

    return crop_size_pix, microns_per_degree, pixels_per_degree


def get_modalities(filename, folder):
    base_end = filename.rfind("_") + 1
    mod_end = filename.rfind(".")

    base_name = filename[0:base_end]
    primary_modality = filename[base_end:mod_end]

    modalities = []
    for file in os.listdir(folder):
        if file.endswith('.tif'):
            path = os.path.join(folder, file)
            if os.path.isfile(path):
                mod_start = file.rfind("_") + 1
                mod_end = file.rfind(".")
                modalities.append(file[mod_start:mod_end])

    return modalities, base_name, primary_modality


def get_id_number(filename, underscores_in_id_count):
    underscores = [pos for pos, char in enumerate(filename) if char == "_"]
    id_end = underscores[underscores_in_id_count]
    return filename[0:id_end]


def define_parameters(image_path, eye, settings):
    folder, filename = os.path.split(image_path)
    crop_size_pix, microns_per_degree, pixels_per_degree = conversions(settings)
    modalities, base_name, primary_modality = get_modalities(filename, folder)
    id_number = get_id_number(filename, settings["text"]["underscores_in_id_count"])

    return {
        "id_number": id_number,
        "mpp": settings["acquisition"]["mpp"],
        "ppd": pixels_per_degree,
        "crop_size_μm": settings["units"]["crop_size"],
        "axial_length": settings["acquisition"]["axial_length"],
        "eye": eye,
        "image_path": image_path,
        "folder": folder,
        "filename": filename,
        "base_name": base_name,
        "primary_modality": primary_modality,
        "modalities": modalities,
    }
