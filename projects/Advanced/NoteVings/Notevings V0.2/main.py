import tkinter as tk
from tkinter.constants import CHAR
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkms
import pyttsx3 as pyt
import os
import time
import datetime
from pathlib import Path
import re

import concurrent.futures
import multiprocessing
import threading


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.window_height = "600"
        self.window_width = "800"
        self.geometry(self.window_width + "x" + self.window_height)
        self.title("VingNotes")

        # =================================================
        # Styling
        # Main text area------------------
        self.font_style_text = ("candara", 14)
        self.text_area_bg = "#3f3b3b"
        self.text_area_fg = "#fff"
        self.text_area_cursor_color = "#fff"

        # status bar and its items------------------
        self.status_frame_bg = "#808080"
        self.status_items_bg = "#fff"
        self.status_items_fg = "#000"
        self.status_items_font_style = ("candara", 10)
        # ====================================================
        # Key variables

        self.file_extensions_allowed = ['txt', 'py']
        self.full_file_name = ""
        self.file_name = ""
        self.text = ""
        self.file_saved = False
        self.file_name_from_entry = ""
        self.saved_text = ""
        self.live_text = ""
        self.changes_saved = False
        self.engine = pyt.init()  # audio engine to read aloud and save as audio
        self.engine.setProperty(
            "voice", "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0")  # change the voice

        # ----------------------------------------------
        # Menu Items
        self.menu_bar = tk.Menu(self)

        # Menu item - File
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='New', command=self.open_new)
        self.file_menu.add_command(label='Open', command=self.open_file)
        self.file_menu.add_command(label='Save', command=self.save_file)
        self.file_menu.add_command(label='Save as', command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Kill', command=self.exit_window)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        # Menu item - Edit
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label='Cut', command=self.cut_text)
        self.edit_menu.add_command(label='Copy', command=self.copy_text)
        self.edit_menu.add_command(label='Paste', command=self.paste_text)
        self.edit_menu.add_command(label='Clear', command=self.clear_text_area)
        self.menu_bar.add_cascade(label='Edit', menu=self.edit_menu)

        # Menu item - Speak
        self.speak_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.speak_menu.add_command(
            label='Read Alound', command=self.read_aloud)
        self.speak_menu.add_command(
            label='Stop Reading', command=self.stop_reading)
        self.speak_menu.add_command(
            label='Save as mp3', command=self.save_as_mp3)
        self.menu_bar.add_cascade(label='Speak', menu=self.speak_menu)

        # Menu item - Themes
        self.themes_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.themes_menu.add_command(
            label='Sublime', command=self.change_theme_sublime)
        self.themes_menu.add_command(
            label='Notepad', command=self.change_theme_notepad)
        self.themes_menu.add_command(
            label='Abstract', command=self.change_theme_abstact)
        self.themes_menu.add_command(
            label='Dark', command=self.change_theme_dark)
        self.menu_bar.add_cascade(label='Themes', menu=self.themes_menu)

        # Menu item - Help
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label='About', command=self.show_about)
        self.help_menu.add_command(label='Help', command=self.show_help)
        self.menu_bar.add_cascade(label='Help', menu=self.help_menu)

        self.configure(menu=self.menu_bar)

        # ============================================================================
        # Scroll Bar for Text area
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Main Text area

        self.text_area = tk.Text(
            self, bg=self.text_area_bg, font=self.font_style_text, fg=self.text_area_fg, insertbackground=self.text_area_cursor_color,
            yscrollcommand=self.scrollbar.set, undo=True, insertwidth=0.5, selectbackground="#7A7A7A")
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.text_area.yview)

        # ============================================================================

        # Status bar

        self.frame_status_bar = tk.Frame(
            self, width=self.window_width, height=17, bg=self.status_frame_bg, relief=tk.SUNKEN)
        self.frame_status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # ===============================================
        # Status items

        self.label_status = tk.Label(
            self.frame_status_bar, text='Status', bg=self.status_items_bg, fg=self.status_items_fg, font=self.status_items_font_style, pady=-5)
        self.label_status.place(relx=0.005)

        self.entry_file_name = tk.Entry(
            self.frame_status_bar, relief=tk.SUNKEN)
        self.entry_file_name.place(relx=0.24)

        self.label_words = tk.Label(
            self.frame_status_bar, text='Words', bg=self.status_items_bg, fg=self.status_items_fg, font=self.status_items_font_style, pady=-5)
        self.label_words.place(relx=0.60)

        self.label_day = tk.Label(self.frame_status_bar, text='Day', bg=self.status_items_bg,
                                  fg=self.status_items_fg, font=self.status_items_font_style, pady=-5)
        self.label_day.place(relx=0.75)

        self.label_time = tk.Label(
            self.frame_status_bar, text='Time', bg=self.status_items_bg, fg=self.status_items_fg, font=self.status_items_font_style, pady=-5)
        self.label_time.place(relx=0.9)

        # code for status labels that don't require functions

        # code for showing the day on the status label

        today = datetime.datetime.today()
        day_int = today.weekday()  # start at 0 : Monday

        days = ["Monday",
                "Tuesday", "Wednsday", "Thursday", "Friday", "Saturday", "Sunday", ]

        week_day = ""
        for number, day in enumerate(days):
            if day_int == number:
                week_day = day

        self.label_day.configure(text=week_day)

        # ======================================================================
        # Functions for status items
        # ======================================================================

    def show_time(self):
        self.time = time.strftime("%H:%M:%S")
        self.label_time.configure(text=self.time)
        self.label_time.after(200, self.show_time)

    def track_changes(self):
        if self.full_file_name or not self.file_saved:
            self.live_text = str(self.text_area.get(1.0, tk.END))
            if self.saved_text != self.live_text:
                self.label_status.configure(
                    text='Unsaved Changes', bg="#ee5a5a", fg='#fff')
                self.changes_saved = False
            else:
                self.label_status.configure(
                    text='Changes Intact', bg="#22eaaa", fg="#000")
                self.changes_saved = True
        self.label_status.after(1000, self.track_changes)

    def show_words_count(self):
        pattern = re.compile(r'\w*.')

        words_list = pattern.findall(self.live_text)
        self.label_words.configure(
            text="words : " + str(len(words_list)))
        self.label_words.after(2000, self.show_words_count)

    def show_status(self):
        pass

    # ===========================================================================================
    #         Menu items functions
    # ===========================================================================================

    def open_new(self):
        new_app = GUI()
        new_app.show_time()
        new_app.protocol("WM_DELETE_WINDOW", new_app.on_close)
        new_app.track_changes()
        new_app.show_words_count()

        # Key bindings---------------
        new_app.bind("<Control-o>", lambda x: new_app.open_file())
        new_app.bind("<Alt-F4>", lambda x: new_app.on_close())
        new_app.bind("<Control-s>", lambda x: new_app.save_file())
        # edit area ---
        new_app.bind("<Control-c>", lambda x: new_app.copy_text())
        new_app.bind("<Control-x>", lambda x: new_app.cut_text())
        new_app.bind("<Control-v>", lambda x: new_app.paste_text())
        new_app.mainloop()

    def save_as_file(self):
        open_dialog = tkfd.asksaveasfile(mode='w', defaultextension='.txt')
        if open_dialog is None:
            return
        self.text_to_save = str(self.text_area.get(1.0, tk.END))
        open_dialog.write(self.text_to_save)
        self.full_file_name = open_dialog.name
        open_dialog.close()
        self.file_saved = True
        self.saved_text = str(self.text_area.get(1.0, tk.END))

        self.entry_file_name.configure(text='Already Saved', state='disabled')

    def open_file(self):
        path = tkfd.askopenfilename()
        if path:

            self.full_file_name = Path(path)
            self.file_name_with_ext = os.path.basename(self.full_file_name)
            self.file_name = self.file_name_with_ext.split(".")[0]
            self.file_extension = self.file_name_with_ext.split(".")[1]

            if self.file_extension in self.file_extensions_allowed:
                with open(path) as file:
                    self.text = file.read()

                if len(self.text_area.get(1.0, tk.END)) > 1:
                    warning = tkms.askquestion("Warning!",
                                               "Do you want to open in a new Window?")
                    if warning == 'yes':
                        new_app = GUI()
                        # new_window.show_time()
                        new_app.text = self.text
                        new_app.text_in_new_window()
                        new_app.show_time()
                        new_app.protocol("WM_DELETE_WINDOW", app.on_close)
                        new_app.track_changes()
                        new_app.show_words_count()

                        new_app.mainloop()
                    else:
                        self.text_area.delete(1.0, tk.END)
                        self.text_area.insert(1.0, self.text)
                        self.label_status.configure(text='File Opened')
                        self.file_saved = True
                        self.saved_text = str(self.text_area.get(1.0, tk.END))

                else:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, self.text)
                    self.label_status.configure(text='File Opened')
                    self.file_saved = True
                    self.saved_text = str(self.text_area.get(1.0, tk.END))
            else:
                tkms.showinfo("Unknown text type",
                              "The file format is not supported")

    def text_in_new_window(self):
        self.text_area.insert(1.0, self.text)

    def exit_window(self):
        # self.destroy kills the instace, quit quits the application
        self.destroy()

    def save_live_text(self):

        self.text_to_save = str(self.text_area.get(1.0, tk.END))
        with open(self.full_file_name, 'w') as file:
            file.write(self.text_to_save)
        self.file_saved = True
        self.saved_text = str(self.text_area.get(1.0, tk.END))
        self.label_status.configure(text='Changes Saved')

    def save_file(self):
        if self.file_saved:
            self.save_live_text()
        else:
            # to check the entry text
            self.file_name_from_entry = self.entry_file_name.get()
            if self.file_name_from_entry:
                if self.full_file_name:
                    self.full_file_name = os.path.dirname(
                        self.full_file_name) + "\\" + self.file_name_from_entry + ".txt"
                    self.save_live_text()
                    self.saved_text = str(self.text_area.get(1.0, tk.END))
                else:
                    self.full_file_name = os.path.join(
                        os.getcwd(), self.file_name_from_entry + ".txt")
                    self.save_live_text()
                self.label_status.configure(
                    text='Saved in the Current Directory')
                self.file_saved = True
                self.saved_text = str(self.text_area.get(1.0, tk.END))
                self.entry_file_name.configure(state='disabled')

            else:
                tkms.showinfo("Enter the filename",
                              "Please enter the filename in the status bar field")

    # ===========================================================================================
    #         Tools Menu functions
    # ===========================================================================================

    def read_aloud(self):
        if self.live_text == "\n":
            self.engine.say("There is nothing to speak out, My lord")
            self.engine.runAndWait()
        else:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(self.engine.say(self.live_text))
            # self.engine.say(self.live_text)
            self.engine.runAndWait()

    # def read_aloud_thread(self):
    #     process = threading.Thread(self.read_aloud)
    #     process.start()
    #     process.join()

    def stop_reading(self):
        self.engine.stop()

    def save_as_mp3(self):
        self.audio_file_name = self.live_text[:self.live_text.find(
            " ", 10)] + '.mp3'
        self.engine.save_to_file(self.live_text, self.audio_file_name)
        self.engine.runAndWait()
        tkms.showinfo("Audio file saved successfully",
                      "Audio file saved in the current location as '" + self.audio_file_name + "'")


# ===========================================================================================================================

    def cut_text(self):
        self.text_area.event_generate(("<<Cut>>"))

    def copy_text(self):
        self.text_area.event_generate(("<<Copy>>"))

    def paste_text(self):
        self.text_area.event_generate(("<<Paste>>"))

    def clear_text_area(self):
        self.text_area.delete(1.0, tk.END)

    # --------------------------------------------------------------------------------------------

    def change_theme_sublime(self):
        self.text_area.config(font=("helvetica", 12))
        self.text_area.config(bg="#282923")
        self.text_area.config(fg="#fff")
        self.text_area.config(insertbackground="#fff")

        # status bar and its items------------------
        self.frame_status_bar.config(bg="#212121")
        self.label_status.config(
            fg="#fff", bg='#282923', font=("candara", 10))
        self.label_words.config(fg="#fff", bg="#282923",
                                font=("candara", 10))
        self.label_day.config(fg="#fff", bg="#282923",
                              font=("candara", 10))
        self.label_time.config(fg="#fff", bg="#282923",
                               font=("candara", 10))

        # ----------------------------------------
        self.menu_bar.config(bg="#000", fg="#fff")

    def change_theme_notepad(self):
        self.text_area.config(font=("helvetica", 12))
        self.text_area.config(bg="#fff")
        self.text_area.config(fg="#000")
        self.text_area.config(insertbackground="#000")

        # status bar and its items------------------
        self.frame_status_bar.config(bg="#E0E0E0")
        self.label_status.config(
            fg="#000", bg='#E0E0E0', font=("candara", 10), relief=tk.SUNKEN)
        self.label_words.config(fg="#000", bg="#E0E0E0",
                                font=("candara", 10), relief=tk.SUNKEN)
        self.label_day.config(fg="#000", bg="#E0E0E0",
                              font=("candara", 10), relief=tk.SUNKEN)
        self.label_time.config(fg="#000", bg="#E0E0E0",
                               font=("candara", 10), relief=tk.SUNKEN)

        # ----------------------------------------
        self.menu_bar.config(bg="#000", fg="#fff")

    def change_theme_dark(self):
        self.text_area.config(font=("seoge ui", 15))
        self.text_area.config(bg="#000")
        self.text_area.config(fg="#fff")
        self.text_area.config(insertbackground="#fff")

        # status bar and its items------------------
        self.frame_status_bar.config(bg="#000")
        self.label_status.config(
            fg="#fff", bg='#3B3B3B', font=("candara", 10))
        self.label_words.config(fg="#fff", bg="#3B3B3B",
                                font=("candara", 10))
        self.label_day.config(fg="#fff", bg="#3B3B3B",
                              font=("candara", 10))
        self.label_time.config(fg="#fff", bg="#3B3B3B",
                               font=("candara", 10))

        # ----------------------------------------
        self.menu_bar.config(bg="#000", fg="#fff")

    def change_theme_abstact(self):
        self.text_area.config(font=("helvetica", 12))
        self.text_area.config(bg="#0e153a")
        self.text_area.config(fg="#fff")
        self.text_area.config(insertbackground="#fff")

        # status bar and its items------------------
        self.frame_status_bar.config(bg="#22d1ee")
        self.label_status.config(
            fg="#000", bg='#e2f3f5', font=("candara", 10), relief=tk.SUNKEN)
        self.label_words.config(fg="#000", bg="#e2f3f5",
                                font=("candara", 10), relief=tk.SUNKEN)
        self.label_day.config(fg="#000", bg="#e2f3f5",
                              font=("candara", 10), relief=tk.SUNKEN)
        self.label_time.config(fg="#000", bg="#e2f3f5",
                               font=("candara", 10), relief=tk.SUNKEN)

    # ===================================================================================================
    #  menu = Help options
    # ===================================================================================================

    def show_help(self):
        tkms.showinfo(
            "Hi there", "The following keyboards shortcuts work here.\n Ctrl - o : Open \n Ctrl - s : Save \n Alt - F4 : Close")

    def show_about(self):
        tkms.showinfo(
            "VingNotes V1", "Enjoy the First Version of the VingNotes. \n A small but practical note taking app \n\N{COPYRIGHT SIGN} Vings ")

    # ==================================================================================================
    # Handling the closing event
    # ===================================================================================================

    def on_close(self):

        if self.changes_saved or (not self.changes_saved and len(self.live_text) == 1):
            self.destroy()
        else:
            warning = tkms.askquestion(
                "Unsaved Changes", "Changes not saved!!  Discard changes?")
            if warning == "yes":
                self.destroy()
            else:
                return

    # ==================================================================================================
    # Dictionary
    # ==================================================================================================


if __name__ == '__main__':
    app = GUI()
    app.show_time()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.track_changes()
    app.show_words_count()

    # Key bindings---------------
    app.bind("<Control-o>", lambda x: app.open_file())
    app.bind("<Alt-F4>", lambda x: app.on_close())
    app.bind("<Control-s>", lambda x: app.save_file())
    # edit area ---
    app.bind("<Control-c>", lambda x: app.copy_text())
    app.bind("<Control-x>", lambda x: app.cut_text())
    app.bind("<Control-v>", lambda x: app.paste_text())
    app.mainloop()
