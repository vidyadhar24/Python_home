import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

from features import compression

import os
import datetime
import time
from pathlib import Path
import random
from tkinter.constants import COMMAND, NE, NW, S


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
        self.bg_label = '#000'
        self.fg_label = '#fff'
        self.font_label = ('Helvetica', 12, 'bold')
        # -------------------------------------------------------------------
        self.bg_items_status = '#000'
        self.fg_items_status = '#fff'
        self.font_items_status = ('Helvetica', 12, 'bold')

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
        self.f_left.pack(side=tk.LEFT, anchor=NW)

        self.f_right = tk.Frame(
            self, width=395, height=410, bg="#D9D9D9")
        self.f_right.pack(side=tk.RIGHT, anchor=NE)

        self.f_status = tk.Frame(
            self, width=100, height=10,  bg="#A1A5A6")
        self.f_status.pack(side=tk.BOTTOM, anchor=S)

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
            self.f_left, text='APPLY BLUR', width=self.b_width, relief=self.b_style, command=self.blur)
        self.b_blur.place(relx=0.55, rely=0.15)

        self.b_down_scale = tk.Button(
            self.f_left, text='DOWNSCALE', width=self.b_width, relief=self.b_style, command=self.down_scale)
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
            self.f_right, text="This is going to be summary", bg=self.bg_label, fg=self.fg_label, font=self.font_label, wraplength=370)
        self.l_top.place(relx=0, rely=0)

        # ----------------------------------- Bottom Label -----------------------------------------

        self.l_bottom = tk.Label(
            self.f_right, text="This is going to more information about what happened", bg=self.bg_label, fg=self.fg_label, font=self.font_label, wraplength=370)
        self.l_bottom.place(relx=0, rely=0.55)

        # ////////////////////////////////// Status items ////////////////////////////////////////////

        # There are Three labels
        # status = to show the status
        # hint = to show the hint
        # time = to show the time
        # load time = to show the load time

        self.l_status = tk.Label(self.f_status, text="Status", bg=self.bg_items_status,
                                 fg=self.fg_items_status, font=self.font_items_status)
        self.l_status.place(relx=0)

        self.l_load_time = tk.Label(self.f_status, text="Load Time", bg=self.bg_items_status,
                                    fg=self.fg_items_status, font=self.font_items_status)
        self.l_load_time.place(relx=0.15)

        self.l_hint = tk.Label(self.f_status, text="Hints", bg=self.bg_items_status,
                               fg=self.fg_items_status, font=self.font_items_status)
        self.l_hint.place(relx=25)

        self.l_time = tk.Label(self.f_status, text="Time", bg=self.bg_items_status,
                               fg=self.fg_items_status, font=self.font_items_status)
        self.l_time.place(relx=9)

        # ////////////////////////////////// Status items ////////////////////////////////////////////
        # Canvas that looks like a line
        # Normally we create canvas to draw other objects like a line over it. But here canvas itself
        # serves the purpose
        self.canvas = tk.Canvas(self, width=350, height=1, bg='#1A1A1A')
        self.canvas.place(relx=0.47, rely=0.5)

        # ////////////////////////////////// Functions ////////////////////////////////////////////

    def compress(self):
        compression.run_compress_app()

    def convert_jpg_to_png(self):
        pass

    def convert_png_to_jpg(self):
        pass

    def conver_to_bw(self):
        pass

    def blur(self):
        pass

    def down_scale(self):
        pass

    def open_folder(self):
        pass

    def make_a_gif(self):
        pass


if __name__ == '__main__':
    app = GUI()
    app.mainloop()
