import os
from PIL import Image

def set_max_pixels(max_pixels):
    Image.MAX_IMAGE_PIXELS = max_pixels

def conversions(units):
    """
    Converts various ophthalmic measurement units based on given parameters.

    Args:
        units dict containing:
            crop_size (float): The size of the crop area in microns.
            mpp (float): Microns per pixel, a unit for image resolution.
            axial_length (float): Axial length of the eye in millimeters.

    Returns:
        tuple: A tuple containing:
            - crop_size_pix (float): Crop size in pixels.
            - microns_per_degree (float): Microns per degree, calculated based on axial length.
            - pixels_per_degree (float): Pixels per degree, derived from microns per degree and mpp.
    """

    crop_size_pix = units["crop_size"] / units["mpp"]
    microns_per_degree = (units["axial_length"]/units["model_eye_length"]) * units["reference_mpd"]
    pixels_per_degree = microns_per_degree / units["mpp"]
    
    return crop_size_pix, microns_per_degree, pixels_per_degree

def get_modalities(filename, folder):
    """
    Extracts modality information from a given filename within a specified folder.

    Args:
        filename (str): The name of the file from which to extract the modalities.
        folder (str): The folder in which the file is located.

    Returns:
        tuple: A tuple containing:
            - modalities (list of str): List of modalities extracted from filenames.
            - base_name (str): The base name of the file.
            - primary_modality (str): The primary modality extracted from the filename.
    """

    base_end = filename.rfind("_") + 1
    mod_end = filename.rfind(".")

    base_name = filename[0:base_end]
    primary_modality = filename[base_end:mod_end]

    modalities = []

    filenames = os.listdir(folder)
    tifflist = [file for file in filenames if file.endswith('.tif')]

    for file in tifflist:

        path = folder + "//" + file

        if os.path.isfile(path):

            mod_start = file.rfind("_") + 1
            mod_end = file.rfind(".")
            mod_name = file[mod_start:mod_end]
            modalities.append(mod_name)    
            
    return modalities, base_name, primary_modality

def get_id_number(filename, underscores_in_id_count):
    """
    Extracts the ID number from a filename based on the count of underscores.

    Args:
        filename (str): The filename from which to extract the ID number.
        underscores_in_id_count (int): The number of underscores present in the image id

    Returns:
        str: The extracted ID number from the filename.
    """
   
    underscores = [pos for pos, char in enumerate(filename) if char == "_"]
    
    id_end = underscores[underscores_in_id_count]

    id_number = filename[0:id_end]
    
    return id_number

def define_parameters(image_path, eye, settings):
    """
    Defines and returns a dictionary of parameters for image processing.

    Args:
        image_path (str): The path to the image file.
        eye (Eye): The Eye enumeration indicating whether it's the right or left eye.
        settings (dict): A dictionary of settings from the configuration file.

    Returns:
        dict: A dictionary containing various parameters used in image processing.
    """
    
    folder, filename = os.path.split(image_path)
    crop_size_pix, microns_per_degree, pixels_per_degree = conversions(settings["units"])
    modalities, base_name, primary_modality = get_modalities(filename, folder)
    id_number = get_id_number(filename, settings["text"]["underscores_in_id_count"])
    
    parameters = {
        "id_number" : id_number,
        "mpp" : settings["units"]["mpp"],
        "ppd" : pixels_per_degree,
        "crop_size_μm" : settings["units"]["crop_size"],
        "axial_length" : settings["units"]["axial_length"],
        "eye" : eye,
        "image_path" : image_path,
        "folder" : folder,
        "filename" : filename,
        "base_name" : base_name,
        "primary_modality" : primary_modality,
        "modalities": modalities
        }
    
    return parameters