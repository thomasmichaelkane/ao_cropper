class Crosshair:
    """
    A class using a crosshair representing the foveal centre.

    This class is designed to handle the creation and manipulation of a crosshair used for 
    referencing the foveal centre. It provides functionality for marking the crosshair on a 
    canvas, adding degree markers, and calculating related coordinates.

    Attributes:
        coordinates (tuple): The center coordinates of the crosshair.
        top_left (tuple): The top-left coordinates of the window at creation.
        scale (float): The scale (zoom) of the image at creation.
        parameters (dict): User parameters.
        settings (dict): Settings for the crosshair from the external settings module.

    Methods:
        __init__: Initializes the crosshair with specified parameters.
        calculate_length: Calculates the length of the crosshair lines based on the current scale.
        find_original_coordinates: Recalculates the original coordinates of the crosshair based on a new top-left reference.
        update_scale: Updates the scale factor for the crosshair.
        add_degree_markers: Adds degree markers or rings to the crosshair on a canvas.
        mark: Marks the crosshair on a canvas, updating its length and markers.
        get_abs_location: Returns the absolute coordinates of the crosshair center.
        stamp: Stamps the crosshair onto the image.
    """
    
    def __init__(self, coordinates, top_left, scale, parameters, settings):

        self.coordinates = coordinates
        self.top_left = top_left
        self.scale = scale
        
        for k, v in parameters.items():
            setattr(self, k, v)
            
        for k, v in settings.items():
            setattr(self, k, v)

        # create a list of degree marking distances (every 1deg plus one at 0.5deg)
        num_degmarks = int(self.length_pixels / self.ppd)
        self.degree_marks = list(range(-num_degmarks, num_degmarks+1))
        self.degree_marks.append(0.5)
        self.degree_marks.append(-0.5)
        self.degree_marks.remove(0)

        self.x = self.coordinates[0]
        self.y = self.coordinates[1]

        # use the top left corner of window and the scale to find absolute coordinates
        self.x_absolute = (self.x - self.top_left[0]) / self.scale
        self.y_absolute = (self.y - self.top_left[1]) / self.scale

    def calculate_length(self):

        length = self.length_pixels * self.scale

        self.x_min = self.x - length
        self.x_max = self.x + length
        self.y_min = self.y - length
        self.y_max = self.y + length

    def find_original_coordinates(self, new_top_left):

        self.x = (self.x_absolute + (new_top_left[0]/self.scale)) * self.scale
        self.y = (self.y_absolute + (new_top_left[1]/self.scale)) * self.scale

    def update_scale(self, scale):

        self.scale = scale

    def add_degree_markers(self, canvas, rings, new_top_left, replacing=False):

        if not replacing:

            self.find_original_coordinates(new_top_left)

        if rings is False:

            # create small degree markings along the crosshair
            for n in self.degree_marks:

                mark_width_scaled = self.mark_width * self.scale
                radius = n * self.ppd * self.scale

                x = radius + self.x
                y = radius + self.y

                x_left = self.x - mark_width_scaled
                x_right = self.x + mark_width_scaled
                y_top = self.y - mark_width_scaled
                y_bottom = self.y + mark_width_scaled
                canvas.create_line(x_left, y, x_right, y, tags=("crosshair", "markers"), fill=self.colour)
                canvas.create_line(x, y_top, x, y_bottom, tags=("crosshair", "markers"), fill=self.colour)

        elif rings is True:

            # create circles at the degree distances
            for n in self.degree_marks:

                if n != 0:
                    radius = n * self.ppd * self.scale
                    canvas.create_circle(canvas, self.x, self.y, radius, tags=("crosshair", "rings"), outline=self.colour)

    def mark(self, canvas, rings):

        self.calculate_length()

        self.horizontal = canvas.create_line(self.x_min, self.y, self.x_max, self.y, tags=("crosshair", "cross"), fill=self.colour)
        self.vertical = canvas.create_line(self.x, self.y_min, self.x, self.y_max, tags=("crosshair", "cross"), fill=self.colour)

        self.add_degree_markers(canvas, rings, self.top_left, replacing=True)

    def get_abs_location(self):

        coordinates = (self.x_absolute, self.y_absolute)
        return coordinates

    def stamp(self, image):

        image.line([(self.x_absolute - 10000), self.y_absolute, (self.x_absolute + 10000), self.y_absolute], fill=self.colour, width=4)
        image.line([self.x_absolute, (self.y_absolute - 10000), self.x_absolute, (self.y_absolute + 10000)], fill=self.colour, width=4)

        return image