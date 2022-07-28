import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as tkms
import tinify as tf
import datetime
from pathlib import Path
import os
import time
import threading


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("Vings Image Compressor")

        # styling
        self.font_style = ("Segoe UI", 12)
        self.font_style_status = ("Lucida Sans UnicodeUI", 9)
        self.font_style_summary = ("Segoe UI", 13)
        self.font_style_details = ("Segoe UI", 13, 'bold')

        # resources
        self.source_path = ""
        # filename without extension
        self.file_name = ""
        self.file_extension = ""
        self.file_extensions_allowed = ['jpg', 'png']
        self.destination_dir_name = "Compressed"
        self.compressions_used = 0
        self.history = []
        # menu
        self.parent_menu = tk.Menu(self)

        self.menu_file = tk.Menu(self.parent_menu, tearoff=0)
        self.menu_file.add_command(label='Open', command=self.open_image)
        self.menu_file.add_command(label='History', command=self.show_history)
        self.menu_file.add_command(label='Close', command=quit)
        self.menu_file.add_command(
            label='Open Compressed', command=self.open_compressed)
        self.parent_menu.add_cascade(label='File', menu=self.menu_file)

        self.menu_info = tk.Menu(self.parent_menu, tearoff=0)
        self.menu_info.add_command(label='Help', command=self.show_help)
        self.menu_info.add_command(label='About', command=self.show_info)
        self.parent_menu.add_cascade(label='Info', menu=self.menu_info)

        self.configure(menu=self.parent_menu)

        # Status bar

        self.frame_status = tk.Frame(self, width=600, height=15, bg='#000')
        self.frame_status.pack(side=tk.BOTTOM)

        self.label_status_left = tk.Label(
            self.frame_status, text='Status', pady=-5, font=self.font_style_status, bg="#000", fg="#fff")
        self.label_status_left.place(relx=0.01)

        self.label_status_count = tk.Label(
            self.frame_status, text='Count', pady=-5, font=self.font_style_status, bg="#000", fg="#fff")
        self.label_status_count.place(relx=0.61)

        self.label_status_day = tk.Label(
            self.frame_status, text='Time', pady=-5, font=self.font_style_status, bg="#000", fg="#fff")
        self.label_status_day.place(relx=0.78)

        self.label_status_time = tk.Label(
            self.frame_status, text='Count', pady=-5, font=self.font_style_status, bg="#000", fg="#fff")
        self.label_status_time.place(relx=0.90)

        # code for showing the day on the status label

        today = datetime.datetime.today()
        day_int = today.weekday()  # start at 0 : Monday

        days = ["Monday",
                "Tuesday", "Wednsday", "Thursday", "Friday", "Saturday", "Sunday", ]

        week_day = ""
        for number, day in enumerate(days):
            if day_int == number:
                week_day = day

        self.label_status_day.configure(text=week_day)

        # buttons------------

        self.frame_buttons = tk.Frame(
            self, width=600, height=150, bg="#4b89ac")
        self.frame_buttons.pack(side=tk.TOP)
        # other wise, frame is shrunk to fit its content
        self.frame_buttons.pack_propagate(0)

        self.btn_open = tk.Button(
            self.frame_buttons, text='Open', padx=10, pady=10, font=self.font_style, bg="#ace6f6", relief=tk.RIDGE, command=self.open_image)
        self.btn_open.place(relx=0.15, rely=0.3)

        self.btn_compress = tk.Button(
            self.frame_buttons, text='Compress', padx=10, pady=10, font=self.font_style, bg="#ace6f6", relief=tk.RIDGE, command=self.compress_thread)
        self.btn_compress.place(relx=0.41, rely=0.3)

        self.btn_History = tk.Button(
            self.frame_buttons, text='History', padx=10, pady=10, font=self.font_style, bg="#ace6f6", relief=tk.RIDGE, command=self.show_history)
        self.btn_History.place(relx=0.75, rely=0.3)
        # ---------------------------------------------------------

        # canvas to show the result which is devided into two frames
        # one for summary and other for metadata

        # summary frame and labels
        self.frame_summary = tk.Frame(
            self, width=300, height=235, bg="#dee1ec")
        self.frame_summary.pack(side=tk.LEFT)

        # Heading
        self.label_summary_heading = tk.Label(
            self.frame_summary, text="Information", font=("candara", 14, "bold"), bg="#ace6f6")
        self.label_summary_heading.place(x=10, y=10)
        # Label for summary
        self.label_summary = tk.Label(
            self.frame_summary, font=self.font_style_summary, bg="#dee1ec")
        self.label_summary.place(x=30, y=80)

        # Details frame and labels
        self.frame_details = tk.Frame(
            self, width=300, height=235, bg="#eac100")
        self.frame_details.pack(side=tk.RIGHT)
        # Heading
        self.label_details_heading = tk.Label(
            self.frame_details, text="Metadata", font=("candara", 14, "bold"), bg="#ace6f6")
        self.label_details_heading.place(x=10, y=10)

        # Label for details
        self.label_details = tk.Label(
            self.frame_details, font=self.font_style_details, bg="#eac100")
        self.label_details.place(x=50, y=70)
        self.show_time()

    def open_image(self):
        path = filedialog.askopenfilename()
        if path:

            self.source_path = Path(path)
            self.file_name_with_ext = os.path.basename(self.source_path)
            self.file_name = self.file_name_with_ext.split(".")[0]
            self.file_extension = self.file_name_with_ext.split(".")[1]

            if self.file_extension in self.file_extensions_allowed:
                self.label_summary.configure(
                    text="Image Loaded Succesfully")
                self.label_status_left.configure(text="Ready")

            else:
                self.label_summary.configure(
                    text="Image format not yet supported")
                self.label_status_left.configure(text="Failed")
        else:
            self.label_summary.configure(text="Please select an Image")

    def compress_thread(self):
        t1 = threading.Thread(target=self.compress)
        t1.start()

    def compress(self):

        if not self.source_path:
            self.label_summary.configure(
                text="No Image is Selected!!\nOpen an Image first.")
        else:
            self.time_start = time.perf_counter()

            self.label_status_left.config(text="In Progress")
            self.label_summary.configure(text="Image is being processed..")
            with open('..//key.txt') as file:
                key = file.read()

                tf.key = key

            self.source_image = tf.from_file(self.source_path)

            if self.destination_dir_name in os.listdir():
                self.directory = self.destination_dir_name
            else:
                os.makedirs(self.destination_dir_name)
                self.directory = self.destination_dir_name

            self.target_path = self.directory + "/" + \
                self.destination_dir_name + "_" + self.file_name_with_ext

            self.source_image.to_file(self.target_path)

            self.time_ended = time.perf_counter()
            self.label_summary.configure(
                text="Compression Successful. \n Open Target from File Menu")
            self.label_status_left.configure(text="Done")
            self.compressions_used = tf.compression_count
            self.label_status_count.configure(
                text=f'Availabe: {500 - self.compressions_used}')
            self.history.append(self.file_name_with_ext)

            # Showing Metadata

            self.source_image_size = round(
                os.path.getsize(self.source_path)/1024/1024, 2)
            self.target_image_size = round(
                os.path.getsize(self.target_path)/1024/1024, 2)

            self.size_reduced_by = round(
                self.target_image_size - self.source_image_size, 2)
            self.size_reduced_percentage = round(
                self.target_image_size/self.source_image_size * 100)

            self.time_taken = round(self.time_ended - self.time_start, 3)
            self.source_path = ""

            self.metadata = f"Original    : {self.source_image_size} mb    \nCompressed  : {self.target_image_size} mb    \nReduction   : {self.size_reduced_by} ({self.size_reduced_percentage}%)\nTime Taken  : {self.time_taken} sec   "

            self.label_details.config(text=self.metadata)

    def show_history(self):
        if self.history:
            result = ""

            for serial, item in enumerate(self.history, start=1):
                result += str(serial) + ". " + item
                result += "\n"
            self.label_summary.config(text=result)
        else:
            self.label_summary.config(text="No history items present!")

    # Funtions for status
    def show_time(self):
        self.time = time.strftime("%H:%M:%S")
        self.label_status_time.configure(text=self.time)
        self.label_status_time.after(200, self.show_time)

    # Functions for Menu items

    def open_compressed(self):
        if self.destination_dir_name in os.listdir():
            os.startfile(self.destination_dir_name)
        else:
            self.label_summary.config(text="Target directory doesn't exist")

    def show_help(self):
        tkms.showinfo("Help", "Visit the website for more information")

    def show_info(self):
        tkms.showinfo(
            "About", "Vings Image Compressor \n V 0.1.\n\N{COPYRIGHT SIGN} Vings.")


if __name__ == '__main__':
    app = App()
    app.show_time()
    app.mainloop()
