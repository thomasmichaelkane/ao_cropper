import os
import datetime
import csv
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont

class ControlPanel(ttk.Frame):
    """
    A comprehensive control panel interface for the ao cropper application.

    This class extends ttk.Frame and is responsible for creating and managing the GUI components. The
    control panel shows input information along with the coordinates and details of all the crop boxes
    placed so far. It also has buttons for various other functions such as deleting and repositioning.

    Attributes:
        master (tk.Tk): The parent widget.
        cropper (Cropper): The cropper gui object.
        parameters (dict): A dictionary of parameters.
        settings (dict): Additional settings from the config file.

    Methods:
        __init__: Initializes the control panel and its components.
        replace_centre: Removes and replaces the current centre of the image crop.
        toggle_rings: Toggles between showing rings or markers on the image.
        enable_buttons: Enables various control buttons in the UI.
        add_crop: Adds a new crop to the list of crops.
        delete_crop: Deletes a specific crop from the list.
        delete_all_crops: Clears all crops from the list.
        update_coords: Updates the coordinates of the crop locations.
        create_results_folders: Creates folders for saving the results.
        create_locations_csv: Generates a CSV file of crop locations.
        create_canvas_tiff: Creates a TIFF image of the canvas.
        create_crop_tiffs: Generates TIFF images for each crop.
        create_lut: Creates a Look-Up Table (LUT) CSV file.
        save: Saves all the crops and associated files.
        save_close: Saves and closes the application.
        close: Closes the application.
    """

    def __init__(self, master, cropper, parameters, settings):

        ttk.Frame.__init__(self, master=master)
        self.master.title("Control Panel")

        self.cropper = cropper

        for k, v in parameters.items():
            setattr(self, k, v)
            
        self.settings = settings

        panes = ttk.PanedWindow(self.master)
        panes.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)

        self.header_pane = ttk.Frame(panes)
        panes.add(self.header_pane)

        # display the filename
        self.file_label = tk.Label(self.header_pane, text="TIFF:")
        self.file_label.grid(row=1, column=1)
        self.file_display = tk.Text(self.header_pane, width=30, height=1)
        self.file_display.grid(row=1, column=2, columnspan=3, sticky="we")
        self.file_display.insert(tk.END, self.filename)

        self.info_pane = ttk.Frame(panes)
        panes.add(self.info_pane)

        # add labels showing subject ID, eye, and primary modality
        self.mm_label = tk.Label(self.info_pane, text=self.id_number, padx=5, pady=5, relief=tk.GROOVE)
        self.mm_label.grid(row=1, column=1, sticky="we")
        self.eye_label = tk.Label(self.info_pane, text=self.eye.name, padx=5, pady=5, relief=tk.GROOVE)
        self.eye_label.grid(row=1, column=2, sticky="we")
        self.eye_label = tk.Label(self.info_pane, text=("AL: " + str(self.axial_length)), padx=5, pady=5, relief=tk.GROOVE)
        self.eye_label.grid(row=1, column=3, sticky="we")
        self.modality_label = tk.Label(self.info_pane, text=self.primary_modality, padx=5, pady=5, relief=tk.GROOVE)
        self.modality_label.grid(row=1, column=4, sticky="we")

        self.controls_pane = ttk.Frame(panes)
        panes.add(self.controls_pane)

        # add buttons to move the centre location, and to toggle rings to markers
        self.move_centre_button = tk.Button(self.controls_pane, text="Move centre", command=self.replace_centre, state=tk.DISABLED)
        self.move_centre_button.grid(row=1, column=1, padx=2, pady=1, sticky="we")
        self.show_rings_toggle_button = tk.Button(self.controls_pane, text="Rings", command=self.toggle_rings, state=tk.DISABLED)
        self.show_rings_toggle_button.grid(row=1, column=2, padx=2, pady=1, sticky="we")

        self.crops_pane = ttk.Frame(panes)
        panes.add(self.crops_pane)

        self.info_separator = ttk.Separator(self.crops_pane)
        self.info_separator.grid(row=1, columnspan=6, sticky="we", pady=6)

        # add a listbox that will contain information on crops as they are laid down
        crop_label_text = "Selected " + str(self.crop_size_μm) + "μm crops"
        self.crop_list_label = tk.Label(self.crops_pane, text=crop_label_text)
        self.crop_list_label.grid(row=2, column=1, columnspan=4)
        self.crop_list = tk.Listbox(self.crops_pane, width=48, height=25)
        self.crop_list.grid(row=3, column=1, columnspan=5)

        self.save_separator = ttk.Separator(self.crops_pane)
        self.save_separator.grid(row=4, columnspan=6, sticky="we", pady=4)

        self.save_pane = ttk.Frame(panes)
        panes.add(self.save_pane)

        # buttons to delete all crops, save and repeat, and save and quit
        self.delete_button = tk.Button(self.save_pane, text="Delete all", command=self.cropper.delete_all)
        self.delete_button.grid(row=1, column=1, padx = 10, pady = 3)
        self.save_button = tk.Button(self.save_pane, text="Save", command=self.save_close)
        self.save_button.grid(row=1, column=2, padx = 10, pady = 3)

        self.font = ImageFont.truetype("arial.ttf", self.settings["text"]["font_size"])

    def replace_centre(self):

        self.cropper.delete_centre()

        self.move_centre_button.config(state=tk.DISABLED)
        self.show_rings_toggle_button.config(state=tk.DISABLED)

    def toggle_rings(self):

        show_rings = self.cropper.toggle_rings()

        if show_rings is True:
            self.show_rings_toggle_button.config(text="Markers")
        elif show_rings is False:
            self.show_rings_toggle_button.config(text="Rings")

    def enable_buttons(self):

        self.move_centre_button.config(state=tk.NORMAL, cursor="hand2")
        self.show_rings_toggle_button.config(state=tk.NORMAL, cursor="hand2")

    def add_crop(self, id, location_tuple):

        location_string = ", ".join(map(str, location_tuple))
        entry = str(id) + ": " + location_string
        self.crop_list.insert(id, entry)

    def delete_crop(self, i):

        self.crop_list.delete(i)

    def delete_all_crops(self):

        self.crop_list.delete(0, tk.END)

    def update_coords(self, new_location):

        number_of_crops = self.crop_list.size()

        self.crop_list.delete(0, tk.END)

        for x in range(0, number_of_crops):

            id = self.cropper.get_crop_IDs(x)
            location_string = ", ".join(map(str, new_location[x]))
            entry = str(id) + ": " + location_string
            self.crop_list.insert(x, entry)

    def create_results_folders(self):

        # create main output folder
        self.output_folder = self.folder + "//" + "ao_crops_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs(self.output_folder)

        # folder to store the crop tifs
        self.crops_folder = self.output_folder + "//Crops"
        os.makedirs(self.crops_folder)

        # folder to store the canvases displaying the crop locations
        self.canvas_folder = self.output_folder + "//Canvases"
        os.makedirs(self.canvas_folder)

        # folders for each modality within the crops folder
        self.crop_modality_folders = {}

        for modality in self.modalities:
            modality_folder = self.crops_folder + "//" + modality
            os.makedirs(modality_folder)
            self.crop_modality_folders[modality] = modality_folder

    def create_locations_csv(self):

        csv_path = self.output_folder + "//" + "crop_location_data.csv"
        header = [("Crop Number", "CoordV (°)", "MeridianV", "CoordH (°)", "MeridianH", "Distance (°)", "Distance (um)", "Centre Pixel (x)", "Centre Pixel (y)")]
        location_data = [crop.get_location_data() for crop in self.final_crops]

        with open(csv_path, "w", newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(header)
            writer.writerows(location_data)

        csvFile.close()
        print("Crop location data CSV saved")

    def create_canvas_tiff(self, modality_path):

        crosshair = self.cropper.get_foveal_centre()

        canvas_grey = Image.open(modality_path)
        canvas_colour = Image.new("RGBA", canvas_grey.size)
        canvas_colour.paste(canvas_grey)
        draw_canvas = ImageDraw.Draw(canvas_colour)

        draw_canvas = crosshair.stamp(draw_canvas)

        return canvas_colour, draw_canvas

    def create_crop_tiffs(self, modality, modality_path, canvas):

        for crop in self.final_crops:

            # create tifs of every crop location in the current modality
            (image, filename) = crop.make_tiff(modality, modality_path)
            image.save(self.crops_folder + "/" + modality + "/" + filename)
            print(filename + " saved")

            # stamp each crop location on to the draw object canvas for this modality
            canvas = crop.stamp(canvas, self.font)

        return canvas

    def create_lut(self):

        lut_data = (self.id_number, self.mpp)
        lut_path = self.output_folder + "//" + "LUT.csv"

        with open(lut_path, "w") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(lut_data)

        csvFile.close()
        print("LUT.csv saved")

    def save(self) :

        print("Saving crops as tiffs...")

        self.create_results_folders()

        self.final_crops = self.cropper.get_crops()

        self.create_locations_csv()

        # create crops/canvases for every modality found in the original folder
        for modality in self.modalities:

            modality_path = self.folder + "/" + self.base_name + modality + ".tif"
            canvas_tiff, canvas_draw = self.create_canvas_tiff(modality_path)
            self.create_crop_tiffs(modality, modality_path, canvas_draw)

            canvas_tiff_name = self.id_number + "_" + self.eye.name + "_crop_locations_" + modality + ".tif"
            canvas_tiff.save(self.canvas_folder+ "//" + canvas_tiff_name)
            print(canvas_tiff_name + " saved")

        self.create_lut()

        print("Saving complete!")

    def save_close(self):

        self.save()
        self.close()

    def close(self):

        self.cropper.master.destroy()


