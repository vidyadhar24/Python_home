import ctypes
import tkinter as tk
from tkinter import image_names, messagebox as mb
from tkinter import filedialog as fd
from tkinter.constants import COMMAND, DISABLED, NE, NW, S
import threading

import os
import datetime
import time
from pathlib import Path
import random
import shutil

import multiprocessing
import concurrent.futures
from typing import MutableMapping
from PIL import Image, ImageFilter

# to increase the graphics quality on windows 10, import the following from ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("720x430")
        self.attributes('-alpha', 0.8)
        self.title("Vings Image Tools")
        self.resizable(False, False)

        # for ease in typing, the following naming style is adopted
        # f_ = for frames
        # l_ = for labels
        # b_ = for buttons
        # s_ = for status

        # ////////////////////////////////// Key Variables ////////////////////////////////////////////

        self.b_width = 15
        self.b_style = 'raised'
        # -------------------------------------------------------------------
        self.bg_label = '#F2B138'
        self.fg_label = '#003F63'
        self.font_label = ('Helvetica', 13, 'bold')
        # -------------------------------------------------------------------
        self.bg_items_status = '#A1A5A6'
        self.fg_items_status = '#fff'
        self.font_items_status = ('Helvetica', 9)
        self.last_operation = ""

        # ////////////////////////////////// Menu ////////////////////////////////////////////
        self.menu_bar = tk.Menu(self)

        # Menu item - File
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='New', command="self.open_new")
        self.file_menu.add_command(label='Open', command="self.open_file")
        self.file_menu.add_command(label='Save', command="self.save_file")
        self.file_menu.add_command(
            label='Save as', command="self.save_as_file")
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Kill', command="self.exit_window")
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        # Menu item - Help
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label='About', command="self.show_about")
        self.help_menu.add_command(label='Help', command="self.show_help")
        self.menu_bar.add_cascade(label='Help', menu=self.help_menu)

        self.configure(menu=self.menu_bar)

        # ////////////////////////////////// Frames ////////////////////////////////////////////

        self.f_left = tk.Frame(self, width=325, height=410, bg="#353D40")
        # self.f_left.pack(side=tk.LEFT, anchor=NW, expand=False)
        self.f_left.place(relx=0, rely=0)

        self.f_right = tk.Frame(
            self, width=395, height=410, bg="#D9D9D9")
        # self.f_right.pack(side=tk.RIGHT, anchor=NE)
        self.f_right.place(relx=0.46, rely=0)

        self.f_status = tk.Frame(
            self, width=720, height=18,  bg="#A1A5A6")
        # self.f_status.pack(side=tk.BOTTOM, fill=tk.X)
        self.f_status.place(relx=0, rely=0.955)

        # ////////////////////////////////// Buttons ////////////////////////////////////////////

        # ----------------------------------- First Row -----------------------------------------

        self.b_compress = tk.Button(
            self.f_left, text='COMPRESS', width=self.b_width, relief=self.b_style, command=self.compress)
        self.b_compress.place(relx=0.10, rely=0.15)

        self.b_jpg_to_png = tk.Button(
            self.f_left, text='JPG To PNG', width=self.b_width, relief=self.b_style, command=self.convert_jpg_to_png)
        self.b_jpg_to_png.place(relx=0.10, rely=0.35)

        self.b_png_to_jpg = tk.Button(
            self.f_left, text='PNG To JPG', width=self.b_width, relief=self.b_style, command=self.convert_png_to_jpg)
        self.b_png_to_jpg.place(relx=0.10, rely=0.55)

        self.b_bw = tk.Button(
            self.f_left, text='BLACK & WHITE', width=self.b_width, relief=self.b_style, command=self.conver_to_bw)
        self.b_bw.place(relx=0.10, rely=0.75)

        # ----------------------------------- Second Row -----------------------------------------

        self.b_blur = tk.Button(
            self.f_left, text='APPLY BLUR', width=self.b_width, relief=self.b_style, command=self.apply_blur)
        self.b_blur.place(relx=0.55, rely=0.15)

        self.b_down_scale = tk.Button(
            self.f_left, text='DOWNSCALE', width=self.b_width, relief=self.b_style, command=self.down_scale, state=DISABLED)
        self.b_down_scale.place(relx=0.55, rely=0.35)

        self.b_open_folder = tk.Button(
            self.f_left, text='Open Target', width=self.b_width, relief=self.b_style, command=self.open_folder)
        self.b_open_folder.place(relx=0.55, rely=0.55)

        self.b_make_a_gif = tk.Button(
            self.f_left, text='MAKE A GIF', width=self.b_width, relief=self.b_style, command=self.make_a_gif)
        self.b_make_a_gif.place(relx=0.55, rely=0.75)

        # ////////////////////////////////// Labels ////////////////////////////////////////////

        # There are two labels
        # top = to show the summary
        # bottom = to show the metadata

        # ----------------------------------- Top Label -----------------------------------------

        self.l_top = tk.Label(
            self.f_right, text="This is going to be summary", bg=self.bg_label, fg=self.fg_label, font=self.font_label, wraplength=300, padx=10, pady=10)
        self.l_top.place(relx=0.15, rely=0.23)

        # ----------------------------------- Bottom Label -----------------------------------------

        self.l_bottom = tk.Label(
            self.f_right, text="This will be additional Information", bg=self.bg_label, fg=self.fg_label, font=self.font_label, wraplength=300, padx=10, pady=10)
        self.l_bottom.place(relx=0.15, rely=0.65)

        # ////////////////////////////////// Status items ////////////////////////////////////////////

        # There are Three labels
        # status = to show the status
        # hint = to show the hint
        # time = to show the time
        # load time = to show the load time

        self.l_status = tk.Label(self.f_status, text="Status", bg=self.bg_items_status,
                                 fg=self.fg_items_status, font=self.font_items_status, pady=-5)
        self.l_status.place(relx=0)

        self.l_hint = tk.Label(self.f_status, text="Hints", bg=self.bg_items_status,
                               fg=self.fg_items_status, font=self.font_items_status, pady=-5)
        self.l_hint.place(relx=0.30)

        self.l_time = tk.Label(self.f_status, text="Time", bg=self.bg_items_status,
                               fg="#333", font=self.font_items_status, pady=-5)
        self.l_time.place(relx=0.9)

        # ////////////////////////////////// Status items ////////////////////////////////////////////
        # Canvas that looks like a line
        # Normally we create canvas to draw other objects like a line over it. But here canvas itself
        # serves the purpose
        self.canvas = tk.Canvas(self, width=350, height=1, bg='#1A1A1A')
        self.canvas.place(relx=0.47, rely=0.5)

        # ------------------------to show the time--------------------------

        # thread_for_time = threading.Thread(self.show_time(), daemon=True)
        # thread_for_time.start()

        self.show_time()

        # ////////////////////////////////// Functions ////////////////////////////////////////////

    def compress(self):
        compression_app = Compression()
        compression_app.mainloop()

    def convert_jpg_to_png(self):
        conversion_app = Conversion()
        conversion_app.convert_jpg_to_png()

    def convert_png_to_jpg(self):
        conversion_app = Conversion()
        conversion_app.convert_png_to_jpg()

    def conver_to_bw(self):
        conversion_app = Conversion()
        conversion_app.convert_to_bw()

    def apply_blur(self):
        app = ApplyBlur()

    def down_scale(self):
        resize_app = Resize()
        resize_app.mainloop()

    def open_folder(self):
        if self.last_operation == 'compression':
            os.startfile(
                "Compressed")
        elif self.last_operation == 'jpg_to_png_conversion':
            os.startfile(
                "Converted_to_jpg")
        elif self.last_operation == 'png_to_jpg_conversion':
            os.startfile(
                "Converted_to_png")
        elif self.last_operation == 'black_&_white_conversion':
            os.startfile(
                "Black and White")
        elif self.last_operation == 'blur':
            os.startfile(
                "Blurred")
        elif self.last_operation == 'animation_creation':
            os.startfile(
                "Animations")

        else:
            self.l_top.configure(text="No images have been processed yet!!")
            app.f_status.configure(bg="#f52f42")

    def make_a_gif(self):
        animation_app = MakeaGIF()
        animation_app.mainloop()

    # ---------------------------------functions for status items----------------------------------
    def show_time(self):
        self.time = time.strftime("%H:%M:%S")
        self.l_time.configure(text=self.time)
        self.l_time.after(200, self.show_time)


app = GUI()


# -----------------------------------------------------------------------------------------------------------------------------
# /////////////////////////////////////////////////// Compression ///////////////////////////////////////////////////////////
# -----------------------------------------------------------------------------------------------------------------------------


class Compression(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("500x270")
        self.title("Compress Images")
        self.resizable(False, False)

        self.configure(background='#D9D9D9')

        # self.attributes('-topmost',True)
        # it moves the window to the middle of the screen after it loads the images
        self.geometry('+400+250')

        # ///////////////////////////////  Key variables ///////////////////////////////

        self.font = ('Candara', 12, 'bold')

        self.files_names_allowed = []
        self.files_names_not_allowed = []
        self.files_allowed = []

        self.compressed_images = []
        self.default_quality = 25
        self.bg_widgets = "#353D40"
        self.fg_widgets = "#D9D9D9"

        # ///////////////////////////////  Widgets ///////////////////////////////
        # ------------------------------------------------------------------------

        self.b_open_images = tk.Button(
            self, width=15, relief=tk.RAISED, text='Open Images', font=self.font, command=self.open_images, bg=self.bg_widgets, fg=self.fg_widgets)
        self.b_open_images.place(relx=0.07, rely=0.3)

        self.l_quality = tk.Label(
            self, text='Choose Quality', font=self.font, bg="#D9D9D9")
        self.l_quality.place(relx=0.45, rely=0.3)

        # self.e_given_quality = tk.Entry(self)
        # self.e_given_quality.place(relx=0.70, rely=0.325)

        self.slider = tk.Scale(self, from_=0, to=100,
                               orient=tk.HORIZONTAL, bg=self.bg_widgets, fg=self.fg_widgets)
        self.slider.place(relx=0.70, rely=0.28)
        self.slider.set(self.default_quality)

        self.b_compress = tk.Button(self, text='Compress',
                                    width=15, relief=tk.RAISED, font=self.font, command=self.compress, bg=self.bg_widgets, fg=self.fg_widgets)
        self.b_compress.place(relx=0.36, rely=0.80)

        # ------------------------------- Canvas to draw a line -------------------

        self.canvas = tk.Canvas(self, width=350, height=1, bg='#1A1A1A')
        self.canvas.place(relx=0.15, rely=0.70)

        # ///////////////////////////////  Functions ///////////////////////////////

    def open_images(self):
        self.images_list = fd.askopenfilenames()
        if not self.images_list:
            app.l_top.configure(text="No Image Selected!! Please select one")
            app.f_status.configure(bg="#f52f42")
            self.destroy()
        else:
            for image in self.images_list:
                file_name = os.path.basename(image)
                if file_name.split(".")[1] in ['jpg', 'JPG']:
                    self.files_names_allowed.append(file_name)
                    self.files_allowed.append(image)
                else:
                    self.files_names_not_allowed.append(file_name)

        # The following checks if the given images are compatible
            if not self.files_names_allowed:  # if no file is a jpeg
                app.l_top.configure(
                    text="Only 'jpg' images can be compressed!!")
                self.destroy()
            else:
                self.attributes('-topmost', 1)
                self.no_of_allowed_files = len(self.files_allowed)
                app.l_top.configure(
                    text=str(self.no_of_allowed_files) + " images have been loaded successfully")
            if 'Compressed' not in os.listdir():
                os.makedirs('Compressed')
            else:
                shutil.rmtree('Compressed')
                os.makedirs('Compressed')

            self.size_before_compression = 0

            for item in self.files_allowed:
                item_size = os.path.getsize(item)
                self.size_before_compression += item_size / \
                    1024/1024  # converting the values to mb

    def compress_images(self, image):

        img = Image.open(image)
        file_name = 'Compressed\\Compressed_' + \
            str(self.quality_selected)+"%_" + os.path.basename(image)
        img.save(file_name, 'JPEG', optimize=True,
                 quality=self.quality_selected)

    def compress(self):

        if not self.files_allowed:
            app.l_top.configure(
                text="No files have been selected for compression")
        else:
            start_time = time.perf_counter()
            self.quality_selected = self.slider.get()
            app.l_top.configure(
                text=str(self.no_of_allowed_files) + " image(s) are being compressed")

            self.destroy()

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.compress_images,
                             self.files_allowed)

            end_time = time.perf_counter()
            self.time_taken = round(end_time - start_time, 2)
            self.size_after_compression = 0
            for item in os.listdir('Compressed'):
                item_size = os.path.getsize(
                    os.path.abspath('Compressed\\' + item))
                self.size_after_compression += item_size / 1024/1024
            app.last_operation = "compression"
            app.f_status.configure(bg="#25993F")
            app.l_top.configure(
                text=str(self.no_of_allowed_files) + " image(s) have been successfully compressed")

            app.l_bottom.configure(
                text=f'Time taken : {self.time_taken} \n Size before compression : {round(self.size_before_compression,2)} \n Size after compression: {round(self.size_after_compression,2)}')


# -----------------------------------------------------------------------------------------------------------------------------
# /////////////////////////////////////////////////// Conversion : JPG to PNG /////////////////////////////////////////////////
# -----------------------------------------------------------------------------------------------------------------------------

class Conversion():
    def __init__(self):
        pass

    def convert_images_to_png(self, image):
        print(os.getpid())

        img = Image.open(image)
        file_name = os.path.basename(image).split(".")[0] + ".png"
        img.save('Converted_to_png\\' + file_name)

    def open_files(self):
        self.files_from_dialog = ()
        self.files_names_allowed = []
        self.files_names_not_allowed = []
        self.files_allowed = []

        self.files_from_dialog = fd.askopenfilenames()
        if not self.files_from_dialog:
            app.l_top.configure(
                text="No Files selected!! \n Please select one")
            app.f_status.configure(bg="#f52f42")
        else:
            for image in self.files_from_dialog:
                file_name = os.path.basename(image)
                if file_name.split(".")[1] in ['jpg', 'JPG', 'png']:
                    self.files_names_allowed.append(file_name)
                    self.files_allowed.append(image)
                    self.no_of_files = len(self.files_allowed)
                else:
                    self.files_names_not_allowed.append(file_name)

    def convert_jpg_to_png(self):
        self.open_files()
        if not self.files_allowed:
            app.l_top.configure(
                text=f'No files selected for conversion')
            app.f_status.configure(bg="#f52f42")
        else:

            if 'Converted_to_png' not in os.listdir():
                os.makedirs('Converted_to_png')
            start_time = time.perf_counter()

            # p = multiprocessing.Pool()
            # result = p.map(self.convert_images, self.allowed_jpgs)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.convert_images_to_png, self.files_allowed)

            end_time = time.perf_counter()
            time_taken = round(end_time - start_time, 2)

            app.last_operation = "jpg_to_png_conversion"

            app.l_top.configure(
                text=f'{self.no_of_files} image(s) Converted Successfully to png')
            app.f_status.configure(bg="#25993F")

            app.l_bottom.configure(
                text='Time Taken: ' + str(time_taken) + "sec")

# ------------------------------------ png to jpeg ----------------------------------

    def convert_images_to_jpg(self, image):
        print(os.getpid())

        img = Image.open(image)
        file_name = os.path.basename(image).split(".")[0] + ".jpg"
        img.save('Converted_to_jpg\\' + file_name)

    def convert_png_to_jpg(self):
        self.open_files()
        if not self.files_allowed:
            app.l_top.configure(
                text=f'No files selected for conversion')
            app.f_status.configure(bg="#f52f42")

        else:

            start_time = time.perf_counter()

            # open_files takes in all the images that include pngs and imgs

            self.allowed_pngs = []

            if 'Converted_to_jpg' not in os.listdir():
                os.makedirs('Converted_to_jpg')

            for item in self.files_allowed:
                if item.endswith('png'):
                    self.allowed_pngs.append(item)

            self.no_of_files = len(self.allowed_pngs)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.convert_images_to_jpg, self.allowed_pngs)

            end_time = time.perf_counter()
            time_taken = round(end_time - start_time, 2)

            app.last_operation = "png_to_jpg_conversion"
            app.l_top.configure(
                text=f'{self.no_of_files} image(s) Converted Successfully to jpg')
            app.f_status.configure(bg="#25993F")

            app.l_bottom.configure(
                text='Time Taken: ' + str(time_taken) + "sec")

        # ----------------------------- to black and white -------------------

    def convert_images_to_bw(self, image):

        img = Image.open(image)
        file_name = os.path.basename(image).split(".")[0] + ".jpg"
        img = img.convert('L')

        img.save('Black and White\\' + file_name)

    def convert_to_bw(self):
        self.open_files()
        if not self.files_allowed:
            app.l_top.configure(
                text=f'No files selected for conversion')
            app.f_status.configure(bg="#f52f42")
        else:

            start_time = time.perf_counter()

            if 'Black and White' not in os.listdir():
                os.makedirs('Black and White')

            self.no_of_files = len(self.files_allowed)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.convert_images_to_bw, self.files_allowed)

            end_time = time.perf_counter()
            time_taken = round(end_time - start_time, 2)

            app.last_operation = "black_&_white_conversion"

            app.l_top.configure(
                text=f'{self.no_of_files} image(s) Converted Successfully to Black and White')
            app.f_status.configure(bg="#25993F")

            app.l_bottom.configure(
                text='Time Taken: ' + str(time_taken) + "sec")


# -----------------------------------------------------------------------------------------------------------------------------
# /////////////////////////////////////////////////// Conversion : JPG to PNG /////////////////////////////////////////////////
# -----------------------------------------------------------------------------------------------------------------------------

class ApplyBlur():
    def __init__(self):

        self.instance = Compression()
        self.instance.l_quality.configure(text='Blur Level')
        self.instance.title("Blur Images")

        self.instance.b_open_images.configure(command=self.open_images)

        # overriding the method of compression to facilitate a different functionlaity
        self.instance.b_compress.configure(
            text='Apply Blur', command=self.apply_blur)

        self.instance.mainloop()

    def open_images(self):
        self.instance.images_list = fd.askopenfilenames()
        if not self.instance.images_list:
            app.l_top.configure(text="No Image Selected!! Please select one")
            app.f_status.configure(bg="#f52f42")
            self.instance.destroy()
        else:
            for image in self.instance.images_list:
                file_name = os.path.basename(image)
                if file_name.split(".")[1] in ['jpg', 'JPG', 'png']:
                    self.instance.files_names_allowed.append(file_name)
                    self.instance.files_allowed.append(image)
                else:
                    self.instance.files_names_not_allowed.append(file_name)

        # The following checks if the given images are compatible
            if not self.instance.files_names_allowed:  # if no file is a jpeg or a png
                app.l_top.configure(
                    text="Only 'jpg' or 'png' images can be blurred!!")
                app.f_status.configure(bg="#f52f42")
                self.instance.destroy()
            else:
                self.instance.attributes('-topmost', 1)
                self.instance.no_of_allowed_files = len(
                    self.instance.files_allowed)
                app.l_top.configure(
                    text=str(self.instance.no_of_allowed_files) + " images have been loaded successfully")

    def blur_images(self, image):

        img = Image.open(image)
        file_name = 'Blurred\\Blurred_@' + \
            str(self.instance.quality_selected)+"%_" + os.path.basename(image)

        img = img.filter(ImageFilter.GaussianBlur(
            self.instance.quality_selected))

        img.save(file_name)

    def apply_blur(self):

        if not self.instance.files_allowed:
            app.l_top.configure(
                text="No files have been selected to blur")
            app.f_status.configure(bg="#f52f42")
        else:
            start_time = time.perf_counter()

            if 'Blurred' not in os.listdir():
                os.makedirs('Blurred')

            self.instance.quality_selected = self.instance.slider.get()

            app.l_top.configure(
                text=str(self.instance.no_of_allowed_files) + " image(s) are being blurred")

            self.instance.destroy()

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.blur_images,
                             self.instance.files_allowed)

            end_time = time.perf_counter()

            self.time_taken = round(end_time - start_time, 2)

            app.last_operation = "blur"

            app.l_top.configure(
                text=str(self.instance.no_of_allowed_files) + " image(s) have been successfully blurred")
            app.f_status.configure(bg="#25993F")
            app.l_bottom.configure(
                text='Time Taken: ' + str(self.time_taken) + "sec")

# -----------------------------------------------------------------------------------------------------------------------------
# /////////////////////////////////////////////////// Resize and downscale /////////////////////////////////////////////////
# -----------------------------------------------------------------------------------------------------------------------------


'''
in the resize functio below,
img = img.thumbnail(
            self.resize_dimensions, Image.LANCZOS)
self.resize_dimensions is not taking values from varible as above.
but it is working fine, when a value is explicitly given like (500,500)

'''


class Resize(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("500x270")
        self.title("Compress Images")
        self.resizable(False, False)

        # it moves the window to the middle of the screen after it loads the images
        self.geometry('+400+250')

    # ///////////////////////////////  Key variables ///////////////////////////////

        self.font = ('Candara', 12, 'bold')

        # self.files_names_allowed = []
        # self.files_names_not_allowed = []
        # self.files_allowed = []

        self.resized_images = []
        self.image_width_to_resize = 0
        self.image_height_to_resize = 0

        # ///////////////////////////////  Widgets ///////////////////////////////
        # ------------------------------------------------------------------------

        self.b_open_images = tk.Button(
            self, width=15, relief=tk.RAISED, text='Open Images', font=self.font, command=self.open_images)
        self.b_open_images.place(relx=0.07, rely=0.3)

        self.l_width = tk.Label(self, text='Choose Width', font=self.font)
        self.l_width.place(relx=0.42, rely=0.3)

        self.l_height = tk.Label(self, text='Choose Height', font=self.font)
        self.l_height.place(relx=0.42, rely=0.55)

        self.e_given_width = tk.Entry(self, text='500')
        self.e_given_width.place(relx=0.68, rely=0.3)
        self.e_given_width.insert(0, '500')

        self.e_given_height = tk.Entry(self)
        self.e_given_height.place(relx=0.68, rely=0.55)
        self.e_given_height.insert(0, '500')

        self.b_resize = tk.Button(self, text='Resize',
                                  width=15, relief=tk.RAISED, font=self.font, command=self.resize)
        self.b_resize.place(relx=0.36, rely=0.80)

        # ------------------------------- Canvas to draw a line -------------------

        self.canvas = tk.Canvas(self, width=350, height=1, bg='#1A1A1A')
        self.canvas.place(relx=0.15, rely=0.70)

        # ///////////////////////////////  Functions ///////////////////////////////

    def open_images(self):
        commons = Common_Features()

        self.allowed_images = []

        if 'Resized' not in os.listdir():
            os.makedirs('Resized')

        for item in commons.files_allowed:
            if item.endswith('jpg') or item.endswith('png'):
                self.allowed_images.append(item)

        self.no_of_files = len(self.allowed_images)

        # self.attributes('-topmost', 1)
        self.attributes('-topmost', 1)

    def resize_images(self, image):
        img = Image.open(image)
        print(self.allowed_images)
        print(self.resize_dimensions)

        local_dimensions = self.resize_dimensions

        file_name = 'Resized\\Resized_' + \
            str(self.image_width_to_resize) + "x" + \
            str(self.image_height_to_resize) + os.path.basename(image)
        img = img.thumbnail(
            self.resize_dimensions, Image.LANCZOS)

        print("dgfgdfdgdf")
        img.save(file_name)

    def resize(self):

        if not self.allowed_images:
            app.l_top.configure(
                text="No files have been selected to resize")
            # self.destroy()
        else:

            start_time = time.perf_counter()

            self.image_height_to_resize = self.e_given_height.get()
            self.image_width_to_resize = self.e_given_width.get()

            self.resize_dimensions = (
                self.image_width_to_resize, self.image_height_to_resize)

            app.l_top.configure(
                text=str(self.no_of_files) + " image(s) are being compressed")

            self.destroy()

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.resize_images, self.allowed_images)

            end_time = time.perf_counter()
            self.time_taken = round(end_time - start_time, 2)

            app.l_top.configure(
                text=str(self.no_of_files) + " image(s) have been successfully resized to " + str(self.image_width_to_resize) + "x" +
                str(self.image_height_to_resize))
            app.l_bottom.configure(
                text=f'Time taken : {self.time_taken}')


# -----------------------------------------------------------------------------------------------------------------------------
# /////////////////////////////////////////////////// Make a gif /////////////////////////////////////////////////
# -----------------------------------------------------------------------------------------------------------------------------


class MakeaGIF(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("500x270")
        self.title("Make a GIF from Images")
        self.resizable(False, False)
        self.configure(background='#D9D9D9')

        # it moves the window to the middle of the screen after it loads the images
        self.geometry('+400+250')

    # ///////////////////////////////  Key variables ///////////////////////////////

        self.font = ('Candara', 12, 'bold')
        self.bg_widgets = "#353D40"
        self.fg_widgets = "#D9D9D9"

        self.no_of_loops = 0
        self.duration = 0

        self.files_from_dialog = ()
        self.files_names_allowed = []
        self.files_names_not_allowed = []
        self.files_allowed = []

        # ///////////////////////////////  Widgets ///////////////////////////////
        # ------------------------------------------------------------------------

        self.b_open_images = tk.Button(
            self, width=15, relief=tk.RAISED, text='Open Images', font=self.font, command=self.open_images, fg=self.fg_widgets, bg=self.bg_widgets)
        self.b_open_images.place(relx=0.07, rely=0.3)

        self.l_no_of_loops = tk.Label(
            self, text='Number of Loops', font=self.font, fg=self.bg_widgets, bg="#D9D9D9")  # bg is given as fg for appeal
        self.l_no_of_loops.place(relx=0.40, rely=0.3)

        self.l_duration = tk.Label(
            self, text='Duration', font=self.font, fg=self.bg_widgets, bg="#D9D9D9")
        self.l_duration.place(relx=0.40, rely=0.55)

        self.slider_loops = tk.Scale(
            self, from_=0, to=20, orient=tk.HORIZONTAL, fg=self.fg_widgets, bg=self.bg_widgets)
        self.slider_loops.place(relx=0.68, rely=0.3)
        self.slider_loops.set(10)  # 10 no of loops in an animation

        self.e_given_duration = tk.Entry(
            self, fg=self.bg_widgets, bg="#D9D9D9")
        self.e_given_duration.place(relx=0.68, rely=0.55)
        self.e_given_duration.insert(0, '5')

        self.b_resize = tk.Button(self, text='Animate',
                                  width=15, relief=tk.RAISED, font=self.font, command=self.animate, fg=self.fg_widgets, bg=self.bg_widgets)
        self.b_resize.place(relx=0.36, rely=0.80)

        # ------------------------------- Canvas to draw a line -------------------

        self.canvas = tk.Canvas(self, width=350, height=1, bg='#1A1A1A')
        self.canvas.place(relx=0.15, rely=0.70)

        # ------------------------------- Canvas to show instrutions -------------------
        self.canvas_instructions = tk.Canvas(
            self, width=100, height=20)
        self.canvas_instructions.place(relx=0.73, rely=0.62)

        self.canvas_instructions.create_text(
            50, 10, text="in millisecs")

        # ///////////////////////////////  Functions ///////////////////////////////

    def open_images(self):

        self.files_from_dialog = fd.askopenfilenames()
        if not self.files_from_dialog:
            app.l_top.configure(
                text="No Files selected!! \n Please select one")
            app.f_status.configure(bg="#f52f42")
        else:
            for image in self.files_from_dialog:
                file_name = os.path.basename(image)
                if file_name.split(".")[1] in ['jpg', 'JPG', 'png']:
                    self.files_names_allowed.append(file_name)
                    self.files_allowed.append(image)
                    self.no_of_files = len(self.files_allowed)
                    app.l_top.configure(
                        text=f'{self.no_of_files} loaded to be an animated gif')
                    self.attributes('-topmost', 1)
                else:
                    self.files_names_not_allowed.append(file_name)

        if 'Animations' not in os.listdir():
            os.makedirs('Animations')

    def animate(self):
        if not self.files_allowed:
            app.l_top.configure(
                text="No FIles available to create an animation")
            app.f_status.configure(bg="#f52f42")
        else:
            self.no_of_files = int(self.slider_loops.get())
            self.duration = int(self.e_given_duration.get())

            self.result = [Image.open(img) for img in self.files_allowed]

            self.target_file_name = self.files_names_allowed[0].split(".")[
                0] + " _animation.gif"

            self.result[0].save("Animations\\" + self.target_file_name, save_all=True,
                                append_images=self.result[1:], optimize=False, duration=self.duration, loop=self.no_of_loops)

            app.last_operation = "animation_creation"
            app.l_top.configure(text=self.target_file_name +
                                " has been created successfully in Animations folder")
            app.f_status.configure(bg="#25993F")
            self.destroy()


if __name__ == '__main__':

    app.mainloop()
