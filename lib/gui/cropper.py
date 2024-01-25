import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from PIL import Image, ImageTk

from lib.gui.auto_scrollbar import AutoScrollbar
from lib.gui.control_panel import ControlPanel
from lib.assets.crosshair import Crosshair
from lib.assets.crop_box import CropBox
from lib.utils.util_func import *

class Cropper(ttk.Frame):
    """
    A zoomable canvas for cropping sections from aoslo iamges efficiently. This is the mother
    class for the AutoScrollBar, ControlPanel, CropBoxes and Crosshairs.

    This class extends ttk.Frame and provides a user interface for handling image cropping, 
    zooming, and annotation. It allows a large image file to be loaded (the canvas) and 
    navigated and zoomed, and crop box markers to be placed anywhere on the image. An eye
    centre is also placed to automatically calculate the true distances of each crop from
    the foveal centre.
    
    Attributes:
        master (tk.Tk): The parent widget.
        parameters (dict): User parameters.

    Methods:
        __init__: Initializes the Cropper interface with image and parameters.
        open_control_panel: Opens the control panel for additional parameters and controls.
        scroll_y: Vertical scrolling action for the canvas.
        scroll_x: Horizontal scrolling action for the canvas.
        move_from: Marks the start position for canvas dragging.
        move_to: Drags the canvas to a new position.
        wheel: Handles zooming in and out of the image with mouse wheel.
        show_image: Displays the image on the canvas, adjusting for zoom and scroll.
        dbutton_click: Handles double-click events for setting crops or foveal center.
        toggle_rings: Toggles the visibility of rings or degree markers on the canvas.
        new_centre: Sets a new foveal center on the canvas.
        delete_centre: Removes the foveal center from the canvas.
        new_crop: Adds a new crop box at the clicked location.
        advance_crop_iterator: Increments the crop box ID iterator.
        delete_crop: Deletes a specified crop box.
        delete_all: Deletes all crop boxes.
        get_image_corners: Returns the corner coordinates of the image.
        get_image_scale: Returns the current scale of the image.
        get_crops: Returns the list of current crop boxes.
        get_crop_IDs: Returns the ID of a specified crop box.
        get_foveal_centre: Returns the current foveal center.
        get_master: Returns the master widget.
    """

    def __init__(self, master, image_path, parameters, settings):

        ttk.Frame.__init__(self, master=master)
        self.master.title("AOSLO Cropper")
        
        self.image_path = image_path

        for k, v in parameters.items():
            setattr(self, k, v)
            
        self.parameters = parameters
        self.settings = settings

        # Vertical and horizontal scrollbars for canvas
        vbar = AutoScrollbar(self.master, orient="vertical")
        hbar = AutoScrollbar(self.master, orient="horizontal")
        vbar.grid(row=0, column=1, sticky="ns")
        hbar.grid(row=1, column=0, sticky="we")

        # Create canvas and put image on it
        self.canvas = tk.Canvas(self.master, highlightthickness=0,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.grid(row=0, column=0, sticky="nswe")
        self.canvas.update()  # wait till canvas is created
        
        def _create_circle(self, x, y, r, **kwargs):
            return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
        
        self.canvas.create_circle = _create_circle
        
        vbar.configure(command=self.scroll_y)  # bind scrollbars to the canvas
        hbar.configure(command=self.scroll_x)

        # Make the canvas expandable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        # Bind events to the Canvas
        self.canvas.bind("<Configure>", self.show_image)  # canvas is resized
        self.canvas.bind("<ButtonPress-1>", self.move_from)
        self.canvas.bind("<B1-Motion>",     self.move_to)
        self.canvas.bind("<MouseWheel>", self.wheel)  # with Windows and MacOS, but not Linux
        self.canvas.bind("<Button-5>",   self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind("<Button-4>",   self.wheel)  # only with Linux, wheel scroll up
        self.canvas.bind("<Double-Button-1>", self.dbutton_click)
        self.canvas.tag_bind("removable", "<ButtonPress-3>", self.delete_crop)

        self.image = Image.open(self.image_path)  # open image
        self.width, self.height = self.image.size
        self.imscale = 1.0  # scale for the canvas image
        self.delta = 2  # zoom magnitude
        self.crop_box_colour = self.settings["crop_box"]["colour"]

        # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.canvas.create_rectangle(0, 0, self.width, self.height, width=0)

        # set up some preliminary booleans and empty lists
        self.centre_is_placed = False
        self.show_rings = False
        self.crop_iterator = 1
        self.foveal_centre = None
        self.crop_IDs = []
        self.crops = []

        self.show_image()
        self.open_control_panel()

    def open_control_panel(self):

        self.control_panel_master = tk.Toplevel(self.master)
        self.control_panel = ControlPanel(self.control_panel_master, self, self.parameters, self.settings)

    def scroll_y(self, *args, **kwargs):

        self.canvas.yview(*args, **kwargs)  # scroll vertically
        self.show_image()  # redraw the image

    def scroll_x(self, *args, **kwargs):

        self.canvas.xview(*args, **kwargs)  # scroll horizontally
        self.show_image()  # redraw the image

    def move_from(self, event):

        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):

        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.show_image()  # redraw the image

    def wheel(self, event):

        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        bbox = self.canvas.bbox(self.container)  # get image area

        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]: pass  # Ok! Inside the image
        else: return  # zoom only inside image area
        scale = 1.0

        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down
            i = min(self.width, self.height)
            if int(i * self.imscale) < 30: return  # image is less than 30 pixels
            self.imscale /= self.delta
            scale        /= self.delta
        if event.num == 4 or event.delta == 120:  # scroll up
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
            if i < self.imscale: return  # 1 pixel is bigger than the visible area
            self.imscale *= self.delta
            scale        *= self.delta

        # hide all marked boxes if zoomed far away
        if self.imscale <= 0.2:
            self.canvas.itemconfigure("box", outline="")
        else:
            self.canvas.itemconfigure("box", outline=self.crop_box_colour)

        self.canvas.scale("all", x, y, scale, scale)  # rescale all canvas objects
        self.show_image()

    def show_image(self, event=None, *kwargs):

        bbox1 = self.canvas.bbox(self.container)  # get image area

        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        
        bbox2 = (self.canvas.canvasx(0),  # get visible area of the canvas
                 self.canvas.canvasy(0),
                 self.canvas.canvasx(self.canvas.winfo_width()),
                 self.canvas.canvasy(self.canvas.winfo_height()))
        
        bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
                max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
        
        if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]
            
        if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]
            
        self.canvas.configure(scrollregion=bbox)  # set scroll region
        
        x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(bbox2[1] - bbox1[1], 0)
        x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
        
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            
            x = min(int(x2 / self.imscale), self.width)   # sometimes it is larger on 1 pixel...
            y = min(int(y2 / self.imscale), self.height)  # ...and sometimes not
            
            image = self.image.crop((int(x1 / self.imscale), int(y1 / self.imscale), x, y))
            imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
            imageid = self.canvas.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
                                               anchor="nw", image=imagetk)
            
            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection
            self.image_corners = bbox1

    def dbutton_click(self, event):

        dclickxy = [self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)]

        if self.centre_is_placed:
            self.new_crop(dclickxy)

        else:
            self.new_centre(dclickxy)

        self.show_image("dbclick")

    def toggle_rings(self):

        self.show_rings = not self.show_rings

        if self.show_rings is True:
            self.canvas.delete("markers")
            
        elif self.show_rings is False:
            self.canvas.delete("rings")

        self.foveal_centre.update_scale(self.imscale)
        self.foveal_centre.add_degree_markers(self.canvas, self.show_rings, self.image_corners[0:2])

        return self.show_rings

    def new_centre(self, location):

        # create new crosshair instance on placement of new centre
        self.foveal_centre = Crosshair(coordinates=location,
                                       top_left=self.image_corners[0:2],
                                       scale=self.imscale,
                                       parameters=self.parameters,
                                       settings=self.settings["crosshair"])

        # mark the crosshair, and record the foveal centre coordinates
        self.foveal_centre.mark(self.canvas, self.show_rings)
        self.centre_abs = self.foveal_centre.get_abs_location()
        self.centre_is_placed = True

        self.control_panel.enable_buttons()

        # relocate all crops in relation to this new centre and update their distances to it
        [x.locate(self.centre_abs) for x in self.crops]
        new_crop_distances = [x.get_round_coordinates(1) for x in self.crops]

        self.control_panel.update_coords(new_crop_distances)

        print('Foveal centre location updated.')

    def delete_centre(self):

        self.canvas.delete("crosshair")
        self.centre_is_placed = False

    def new_crop(self, location):

        # create new crop instance at click location
        self.crops.append(CropBox(ID=self.crop_iterator,
                                   coordinates=location,
                                   top_left=self.image_corners[0:2],
                                   scale=self.imscale,
                                   parameters=self.parameters,
                                   settings=self.settings["crop_box"]))

        # add crop to the cache and contorl panel list
        self.crop_IDs.append(self.crops[-1].get_ID())
        self.crops[-1].mark(self.canvas)
        self.crops[-1].locate(self.centre_abs)

        crop_distance = self.crops[-1].get_round_coordinates(1)

        self.control_panel.add_crop(self.crop_IDs[-1], crop_distance)

        self.advance_crop_iterator()

    def advance_crop_iterator(self):

        self.crop_iterator += 1

    def delete_crop(self, event):

        rclickxy = [self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)]

        try:

            # delete the nearest crop box to right click
            selection = self.canvas.find_closest(rclickxy[0], rclickxy[1])
            select_tags = self.canvas.gettags(selection)
            ID = select_tags[0]

            to_delete = self.canvas.find_withtag(ID)
            self.canvas.delete(ID)

            # delete crop, crop ID, and wipe from control panel list
            index = ID.find("#") + 1
            crop_ID = int(ID[index:])
            i = self.crop_IDs.index(crop_ID)

            self.crops.pop(i)
            self.crop_IDs.pop(i)
            self.control_panel.delete_crop(i)

            print(ID + " was removed.")

        except:

            print("Error: Crop was not removed, please try again.")

    def delete_all(self):

        delete = msg.askquestion("Delete Crops", "Are you sure you want to remove all crops?")

        # delete all crop boxes
        if delete == "yes":
            self.crop_IDs = []
            self.crops = []

            self.control_panel.delete_all_crops()
            self.canvas.delete("removable")
            print("All crops removed.")

    def get_image_corners(self):

        return self.image_corners

    def get_image_scale(self):

        return self.imscale

    def get_crops(self):

        return self.crops

    def get_crop_IDs(self, x):

        return self.crop_IDs[x]

    def get_foveal_centre(self):

        return self.foveal_centre

    def get_master(self):

        return self.master
    

