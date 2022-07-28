import tkinter as tk
from tkinter import filedialog
import datetime
import time
import os
import tinify as tf
from PIL import Image, ImageFilter
from PIL import ImageTk as itk
from pathlib import Path

# Initilaization

root = tk.Tk()
root.title('Vings Image Compressor V0.1')
root.geometry("550x480")
root.resizable(False, False)

# functions -----------------------------------------------


def open_source_image():
    path = filedialog.askopenfilename()

    path = Path(path)
    file_name_with_ext = os.path.basename(path)
    file_name = file_name_with_ext.split(".")[0]
    extension = file_name_with_ext.split(".")[1]
    extensions_allowed = ['jpg', 'png']

    if extension in extensions_allowed:
        with open('files.txt', 'a') as file:
            file.write(str(path))
            file.write("\n")
        label_result.configure(text='Image Loaded Succesfully!')
    else:
        label_result.configure(text='Image format not supported!')


# tinify module and api Initilaization---


with open('key.txt') as file:
    key = file.read()

tf.key = key


def process_image():

    label_result.configure(text='Image is being compressed...')
    with open('files.txt') as file:
        file_path = file.read().split('\n')[-2]
    with open(file_path, 'rb') as file:
        source_image_data = file.read()

    compressed_data = tf.from_buffer(source_image_data).to_buffer()

    destination_dir = "Compressed"
    if destination_dir in os.listdir():
        directory = destination_dir
    else:
        os.makedirs(destination_dir)
        directory = destination_dir

    path = Path(file_path)
    file_name_with_ext = os.path.basename(path)

    target_path = destination_dir + "/Compressed_" + file_name_with_ext
    with open(target_path, 'wb') as file:
        file.write(compressed_data)
    compressions_this_month = tf.compression_count
    label_result.configure(
        text='Image processes successfully \n and downloaded \n \n You have ' + str(500 - compressions_this_month) + ' free compressions \n left this month')


def show_history():
    label_result.configure(text='soemthing')


def open_directory():
    path = "I:\Do\Vings\python__\projects\Advanced\Image Compressor Tinify\Compressed"
    if os.path.exists(path):
        os.startfile(path)
    else:
        label_result.configure('No files present in the directory')


# Layout------------------------------------------------------------

frame_buttons = tk.Frame(root, width=100, height=480,
                         bg="#fcefee", borderwidth=2, relief=tk.GROOVE)
# frame_buttons.pack(side = tk.LEFT)
frame_buttons.place(height=480, width=140, relx=0.05)

btn_open = tk.Button(frame_buttons, bg='#cabbe9', text='Open',
                     padx=40, font=("Helvetica", 12), relief=tk.RAISED, command=open_source_image)
btn_open.place(rely=0.2, relx=0.015)

btn_process = tk.Button(frame_buttons, bg='#cabbe9', text='Process',
                        padx=30, font=("Helvetica", 12), relief=tk.RAISED, command=process_image)
btn_process.place(rely=0.47, relx=0.015)

btn_history = tk.Button(frame_buttons, bg='#cabbe9', text='History',
                        padx=35, font=("Helvetica", 12), relief=tk.RAISED, command=show_history)
btn_history.place(rely=0.75, relx=0.015)


# Area to show the result
frame_result = tk.Frame(root, bg='#808080', width=382,
                        height=250, relief=tk.GROOVE)
frame_result.place(relx=0.305, rely=0.26)


# label for result

label_result = tk.Label(frame_result, bg='#808080',
                        font=("Helvetica", 12, 'bold'))
# label_result.place()
label_result.place(relx=0.25, rely=0.25)


# Button to open for folder
btn_open_target = tk.Button(
    root, text='Open Directory', padx=5, pady=5, command=open_directory)
btn_open_target.place(relx=0.72, rely=0.85)

temp_file = 'files.txt'
if os.path.exists(temp_file):
    os.unlink(temp_file)

root.mainloop()
