import tkinter as tk
from tkinter import filedialog as fd


import os
from pathlib import Path


class compress_app(tk.Tk):

    # class variable to exchange the data between modules

    are_valid_images = ""

    def __init__(self):
        super().__init__()
        self.geometry("500x270")
        self.title("Compress Images")
        self.resizable(False, False)

        # ///////////////////////////////  Key variables ///////////////////////////////

        self.font = ('Candara', 12, 'bold')

        self.files_allowed = ['jpg', 'png']

        # ///////////////////////////////  Widgets ///////////////////////////////
        # ------------------------------------------------------------------------

        self.b_open_images = tk.Button(
            self, width=15, relief=tk.RAISED, text='Open Images', font=self.font, command=self.open_images)
        self.b_open_images.place(relx=0.07, rely=0.3)

        self.l_quality = tk.Label(self, text='Choose Quality', font=self.font)
        self.l_quality.place(relx=0.45, rely=0.3)

        # self.e_given_quality = tk.Entry(self)
        # self.e_given_quality.place(relx=0.70, rely=0.325)

        self.slider = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.slider.place(relx=0.70, rely=0.28)

        self.b_compress = tk.Button(self, text='Compress',
                                    width=15, relief=tk.RAISED, font=self.font, command=self.compress)
        self.b_compress.place(relx=0.36, rely=0.80)

        # ------------------------------- Canvas to draw a line -------------------

        self.canvas = tk.Canvas(self, width=350, height=1, bg='#1A1A1A')
        self.canvas.place(relx=0.15, rely=0.70)

        # ///////////////////////////////  Functions ///////////////////////////////

    def open_images(self):
        compress_app.images_list = fd.askopenfilenames()

        from Reusuables import validation

        validation.validate_images()

        if compress_app.are_valid_images:
            pass
        else:
            from ..main import app
            app.l_top.configure(text="No Image Selected!!, Please select one")
            self.destroy()

    def compress(self):
        pass


def run_compress_app():
    app_compress = compress_app()
    app_compress.mainloop()
