"""Run the AOSLO cropping tool.

This script runs the AOSLO cropping tool with parameters specified
in the configuration file.

Example
-------
Use the command line interface to load a an AOSLO split image file
with scaling and dimensions specified in config.yaml. Here we
are loading from the tiff MM_0364_OS_combined_0p3796umpx_split.tif 
with the Left eye selected::

    $ python run_ao_cropper.py MM_0364_OS_combined_0p3796umpx_split.tif OS

Notes
-----
    The file naming format should be IMAGEID_otherinfo_MODALITY.tif. If
    there are underscores within the ID string, this can be programmed
    using the "underscores_in_id_count" setting in the config file. Other
    tifs in the same folder will be registered as other modalities.

Arguments
----------
image_path : str
    The relative or absolute path to the image file. This
    file should be a (single stack) tiff file.
    
eye : str
    The eye in the image, either "OD" or "OS".
"""

import sys
import tkinter as tk

from lib.gui.cropper import Cropper
from lib.utils import parse
from lib.utils.util_func import *

# main loop
def main():
    
    # parse image path and eye string
    IMAGE_PATH, EYE = parse_args()
    
    # load config settings, parse most important
    SETTINGS = parse.load_config()
    parse.units(SETTINGS["units"])
    
    # calculate further parameters
    parameters = define_parameters(IMAGE_PATH, EYE, SETTINGS)
    
    # increase PIL max image pixels
    set_max_pixels(SETTINGS["units"]["max_image_pixels"])
    
    # run gui
    main = tk.Tk()
    cp = Cropper(main, IMAGE_PATH, parameters, SETTINGS)
    main.mainloop()


def parse_args():

    if len(sys.argv) == 1:
        
        raise KeyError("No image file specified")

    elif len(sys.argv) == 2:
        
        raise KeyError("No eye specified")
        
    elif len(sys.argv) == 3:
        image_path = parse.path(sys.argv[1])
        eye = parse.eye(sys.argv[2])
                      
    else:
        raise KeyError("Too many input arguments")
    
    return image_path, eye

main()