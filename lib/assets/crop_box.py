import math
from PIL import Image

from ..utils.enums import Eye

class CropBox:
    """
    A class representing a specified size crop of an aolso image.

    Attributes:
        ID (int): The identifier for the crop box.
        coordinates (tuple): The center coordinates of the crop box.
        top_left (tuple): The top-left coordinates of the reference area.
        scale (float): The scale (zoom) of the canvas at time of creation.
        parameters (dict): Input parameters.
        settings (dict): Settings for the crop box from the external settings module.

    Methods:
        __init__: Initializes the crop box with specified parameters.
        mark: Marks the crop box on the canvas.
        locate: Calculates the relative location of the crop box to the centre point.
        make_tiff: Creates a TIFF image of the crop area.
        stamp: Stamps the crop box onto an image of the canvas.
        get_round_coordinates: Rounds the coordinates to opthalmic descriptions.
        get_ID: Returns the ID of the crop box.
        get_location_data: Returns the location data of the crop box.
    """
    
    def __init__(self, ID, coordinates, top_left, scale, parameters, settings):

        self.ID = ID
        self.coordinates = coordinates
        self.top_left = top_left
        self.scale = scale
        
        for k, v in parameters.items():
            setattr(self, k, v)
        
        for k, v in settings.items():
            setattr(self, k, v)

        self.OUTLINE_PC = 0.02

        # use top left and scale to get absolute coordinates
        self.x_absolute = (self.coordinates[0] - self.top_left[0]) / self.scale
        self.y_absolute = (self.coordinates[1] - self.top_left[1]) / self.scale

        # round and scale the crop box size
        self.size_pix = self.crop_size_μm / self.mpp
        self.size_pix_scaled = self.size_pix * self.scale
        self.size_pix_round = int(round(self.size_pix))
        self.size_pix_scaled_round = int(round(self.size_pix_scaled))

        # coordinates for the box corners
        self.x0_box = self.coordinates[0] - (self.size_pix_scaled_round * (0.5 - self.OUTLINE_PC/2))
        self.y0_box = self.coordinates[1] - (self.size_pix_scaled_round * (0.5 - self.OUTLINE_PC/2))
        self.x1_box = self.coordinates[0] + (self.size_pix_scaled_round * (0.5 + self.OUTLINE_PC/2))
        self.y1_box = self.coordinates[1] + (self.size_pix_scaled_round * (0.5 + self.OUTLINE_PC/2))

        # cooridnates for the box ID number
        self.x_number = self.coordinates[0] - (self.size_pix_scaled_round * 0.575)
        self.y_number = self.coordinates[1] - (self.size_pix_scaled_round * 0.575)

    def mark(self, canvas):

        # mark the smaller box
        self.outline_pix = int(round(self.size_pix_scaled * self.OUTLINE_PC * (1/self.scale)))

        if self.outline_pix < 1:
            self.outline_pix = 1
        
        self.ID_string = "Crop #" + str(self.ID)

        self.box = canvas.create_rectangle(self.x0_box, 
                                           self.y0_box, 
                                           self.x1_box, 
                                           self.y1_box, 
                                           fill="", 
                                           outline=self.colour, 
                                           width=self.outline_pix, 
                                           tags=(self.ID_string, "removable", "box"), 
                                           activeoutline=self.hover_colour)

        # place number counter next to the box
        number_size = int(self.label_font_size/2)
        
        self.number = canvas.create_text(self.x_number, 
                                         self.y_number, 
                                         fill=self.colour, 
                                         text=self.ID, 
                                         font=("Purisa", number_size), 
                                         tags=(self.ID_string, "removable", "number"), 
                                         activefill=self.hover_colour)

    def locate(self, foveal_centre):

        self.x_relative = self.x_absolute - foveal_centre[0]
        self.y_relative = self.y_absolute - foveal_centre[1]
        self.distance_μm = math.sqrt((self.x_relative**2) + (self.y_relative**2))

        self.x_degrees = self.x_relative / self.ppd
        self.y_degrees = self.y_relative / self.ppd
        self.distance_deg = self.distance_μm / self.ppd

        # flip the x coordinate if eye is OS insteda of OD (used as default)
        if self.eye == Eye.OS:
            self.x_degrees = self.x_degrees * (-1)

        # ophthal coordinates
        if self.x_degrees >= 0:
            self.x_meridian = "N" # nasal
        elif self.x_degrees < 0:
            self.x_meridian = "T" # temporal

        if self.y_degrees >= 0:
            self.y_meridian = "I" # inferior
        elif self.y_degrees < 0:
            self.y_meridian = "S" # superior

        self.x_absolute_deg = math.fabs(self.x_degrees)
        self.x_ophth = (self.x_absolute_deg, self.x_meridian)

        self.y_absolute_deg = math.fabs(self.y_degrees)
        self.y_ophth = (self.y_absolute_deg, self.y_meridian)

    def make_tiff(self, modality, modality_path):

        # corners of the crop
        self.x0 = self.x_absolute - (self.size_pix_round/2)
        self.y0 = self.y_absolute - (self.size_pix_round/2)
        self.x1 = self.x_absolute + (self.size_pix_round/2)
        self.y1 = self.y_absolute + (self.size_pix_round/2)

        # cut the box out of the image
        img = Image.open(modality_path)
        tiff = img.crop((self.x0,self.y0,self.x1,self.y1))

        location_tuple = self.get_round_coordinates(1)
        location_string = ("_".join(map(str, location_tuple))).replace(".","p")

        tiff_name = self.id_number + "_" + self.eye.name + "_" + location_string + "_" + str(self.crop_size_μm) + "μm_crop-" + str(self.ID) + "_" + modality + ".tif"

        return (tiff, tiff_name)

    def stamp(self, image, number_font):

        # draw onto canvas - nudge number along depending on number of digits
        num_digits = len(str(self.ID))
        image.rectangle([self.x0, self.y0, self.x1, self.y1], None, self.colour, width=8)
        image.text([(self.x0 - (30*num_digits)), (self.y0 - 30)], str(self.ID), self.colour, font=number_font)

        return image

    def get_round_coordinates(self, num_dec):

        x_absolute_round = round(self.x_absolute_deg, num_dec)
        if not num_dec: x_absolute_round = int(x_absolute_round)
        y_absolute_round = round(self.y_absolute_deg, num_dec)
        if not num_dec: y_absolute_round = int(y_absolute_round)

        if (x_absolute_round == 0) and (y_absolute_round != 0):
            round_coordinates = ((str(y_absolute_round) + self.y_meridian),)
        elif (x_absolute_round != 0) and (y_absolute_round == 0):
            round_coordinates = ((str(x_absolute_round) + self.x_meridian),)
        elif (x_absolute_round == 0) and (y_absolute_round == 0):
            round_coordinates = ("C",)
        else:
            round_coordinates = (str(y_absolute_round) + self.y_meridian, str(x_absolute_round) + self.x_meridian)

        return round_coordinates

    def get_ID(self):

        return self.ID

    def get_location_data(self):

        location_data = (self.ID, self.y_absolute_deg, self.y_meridian, self.x_absolute_deg, self.x_meridian, self.distance_deg, self.distance_μm, self.x_absolute, self.y_absolute)

        return location_data