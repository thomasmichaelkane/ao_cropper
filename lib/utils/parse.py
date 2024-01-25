import yaml

from .enums import Eye
from . import logging


def load_config():
    """
    Load config file.
    """ 
    
    with open('config.yaml') as config:
        settings = yaml.load(config.read(), Loader=yaml.Loader)
        
    return settings

def units(units):
    """
    Validates units from config file.
    """ 
       
    axial_length(units["axial_length"])
    mpp(units["mpp"])
    crop_size(units["crop_size"])

def path(arg):
    """
    Validates and returns a file path if it points to a TIFF image.
    """  
     
    if arg.endswith(".tif") or arg.endswith(".tiff"):
        
        try:
            file = open(arg)
            file.close()
            return arg
        except FileNotFoundError as err:
            print(err)
            
    else:
        
        raise NameError("The image path needs to point to a TIFF file")

def mpp(arg):
    """
    Validates and returns the 'microns per pixel' value.
    """
    
    try:

        arg = float(arg)

        if not (0.1 < arg < 2):
            logging.warning("microns per pixel is outside the expected range (0.1-2.0mpp)")

    except Exception as e:

        raise ValueError(e)
    
    return arg
    
def eye(arg):
    """
    Validates and returns an Eye enum value for a given string.
    """

    try:
        arg = Eye[arg]
    except:
        raise ValueError("Not a valid eye string - should be OD or OS")
    
    return arg
    
    
def axial_length(arg):
    """
    Validates and returns the axial length.
    """    
    
    try:

        arg = float(arg)

        if not (12 < arg < 40):
            logging.warning("axial length is outside the expected range (12-40mm)")

    except Exception as e:

        raise ValueError(e)
    
    return arg

def crop_size(arg):
    """
    Validates and returns the crop size
    """
    
    try:

        arg = int(arg)

        if not (10 < arg < 400):
            logging.warning("crop size is outside the expected range (10-400μm)")

    except Exception as e:

        raise ValueError(e)
    
    return arg



