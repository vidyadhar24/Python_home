import tkinter as tk
from tkinter.constants import FIRST, INSERT, LEFT
import tkinter.messagebox as tkms
import tkinter.filedialog as tkfd
import requests
import time
from pathlib import Path
import os
import webbrowser


class View_More(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("All Definitions")
        self.geometry("500x300")
        self.resizable(False, False)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text = tk.Text(self, bg="#333", fg="#48E875",
                            yscrollcommand=self.scrollbar.set, font=('Segoe ui', 12))
        self.text.pack(fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.text.yview)

        # self.label = tk.Label(self, bg="#333", fg="#fff", wraplength=380)
        # self.label.pack()


class History(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("History")
        # self.geometry("200x250")
        # the following makes it take the available size based on looping widgets down below
        self.geometry("")
        self.resizable(False, False)


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("600x440")
        self.title("DictVings")
        self.resizable(width=False, height=False)
        self.configure(bg="#555")
        # self.iconphoto(True, tk.PhotoImage(file='dict.png'))

        # ////////////////////// key variables ///////////////////////////////

        self.word = ""
        self.target_location = ""
        self.source_file = ""
        self.counter = 0
        self.definitions = []  # a list to hold the individual definitions in a tuple
        self.font_results = ('Segoe ui', 10, 'bold')
        self.font_headings = ('Candara', 14, "bold")
        self.font_color_headings = "#3EB595"
        self.font_color_results = "#9C3111"
        self.all_definitions = ""
        self.search_history = []
        self.time_taken = ""
        self.file_path = ""
        self.file_name_with_ext = ""
        self.file_name = ""
        self.file_extension = ""
        self.words_from_file = []
        self.error = False
        self.words_unfound = []
        self.words_definitions = {}
        self.target_text = ''
        self.app_url = "https://hungry-edison-3a254b.netlify.app/"

        # ////////////////////// Frames ///////////////////////////////

        self.frame_left = tk.Frame(
            self, width=180, height=400, bg="#222", relief=tk.SUNKEN)
        self.frame_left.pack(side=tk.LEFT, padx=20)

        self.frame_right = tk.Frame(
            self, width=420, height=400, bg="#fff")
        self.frame_right.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.frame_status = tk.Frame(self, bg="#555", height=16, width=600)
        self.frame_status.place(rely=0.964, relx=0)

        # ////////////////////// ENTRY ///////////////////////////////

        self.entry = tk.Entry(self.frame_left, width=25)
        self.entry.place(relx=0.05, rely=0.25)

        # ////////////////////// Labels ///////////////////////////////

        self.label_header = tk.Label(
            self.frame_left, text="DictVings V0.1", bg="#333", font=('Candara', 15), fg="#cdd5d5")
        self.label_header.place(relx=0.11, rely=0.05)

        self.label_instruction = tk.Label(
            self.frame_left, text="Enter the word below", bg="#222", fg="#fff")
        self.label_instruction.place(relx=0.1, rely=0.18)

        self.label_status = tk.Label(
            self.frame_status, text='Ready', bg="#555", fg="#EDEDED", pady=-5)
        self.label_status.place(relx=0.005)

        self.label_info = tk.Label(
            self.frame_status, text='Enter the Word', bg="#555", fg="#EDEDED", pady=-5)
        self.label_info.place(relx=0.4)

        self.label_load_time = tk.Label(
            self.frame_status, bg="#555", fg="#EDEDED", pady=-5)
        self.label_load_time.place(relx=0.82)
        # --------------------------Result label on the right------------------

        self.label_result_type_heading = tk.Label(
            self.frame_right, fg=self.font_color_headings, bg="#fff", font=self.font_headings, wraplength=280, padx=5, justify=tk.LEFT)
        self.label_result_type_heading.place(relx=0, rely=0.05)

        self.label_result_type = tk.Label(
            self.frame_right, fg=self.font_color_results, bg="#fff", font=self.font_results, wraplength=280, padx=8, justify=tk.CENTER, pady=5)
        self.label_result_type.place(relx=0.20, rely=0.05)

        self.label_result_meanging_heading = tk.Label(
            self.frame_right, fg=self.font_color_headings, bg="#fff", font=self.font_headings, wraplength=280, padx=5, justify=tk.LEFT)
        self.label_result_meanging_heading.place(relx=0, rely=0.15)

        self.label_result_meaning = tk.Label(
            self.frame_right, fg=self.font_color_results, bg="#fff", font=self.font_results, wraplength=280, padx=8, justify=tk.CENTER, pady=5)
        self.label_result_meaning.place(relx=0.20, rely=0.15)

        self.label_result_example_heading = tk.Label(
            self.frame_right, fg=self.font_color_headings, bg="#fff", font=self.font_headings, wraplength=280, padx=5, justify=tk.LEFT)
        self.label_result_example_heading.place(relx=0, rely=0.35)

        self.label_result_example = tk.Label(
            self.frame_right, fg=self.font_color_results, bg="#fff", font=self.font_results, wraplength=280, padx=8, justify=tk.CENTER, pady=5)
        self.label_result_example.place(relx=0.20, rely=0.35)

        # --------------------------------- second half ------------------------------------------------

        self.label_result_type_heading_2 = tk.Label(
            self.frame_right, fg=self.font_color_headings, bg="#fff", font=self.font_headings, wraplength=280, padx=5, justify=tk.LEFT)
        self.label_result_type_heading_2.place(relx=0, rely=0.55)

        self.label_result_type_2 = tk.Label(
            self.frame_right, fg=self.font_color_results, bg="#fff", font=self.font_results, wraplength=280, padx=8, justify=tk.CENTER, pady=5)
        self.label_result_type_2.place(relx=0.20, rely=0.55)

        self.label_result_meanging_heading_2 = tk.Label(
            self.frame_right, fg=self.font_color_headings, bg="#fff", font=self.font_headings, wraplength=280, padx=5, justify=tk.LEFT)
        self.label_result_meanging_heading_2.place(relx=0, rely=0.65)

        self.label_result_meaning_2 = tk.Label(
            self.frame_right, fg=self.font_color_results, bg="#fff", font=self.font_results, wraplength=280, padx=8, justify=tk.CENTER, pady=5)
        self.label_result_meaning_2.place(relx=0.20, rely=0.65)

        self.label_result_example_heading_2 = tk.Label(
            self.frame_right, fg=self.font_color_headings, bg="#fff", font=self.font_headings, wraplength=280, padx=5, justify=tk.LEFT)
        self.label_result_example_heading_2.place(relx=0, rely=0.75)

        self.label_result_example_2 = tk.Label(
            self.frame_right, fg=self.font_color_results, bg="#fff", font=self.font_results, wraplength=280, padx=8, justify=tk.CENTER, pady=5)
        self.label_result_example_2.place(relx=0.20, rely=0.75)

        self.labels = [self.label_result_type_heading, self.label_result_type, self.label_result_meanging_heading, self.label_result_meaning, self
                       .label_result_example_heading, self.label_result_example, self.label_result_type_heading_2, self.label_result_type_2, self.label_result_meanging_heading_2, self.label_result_meaning_2, self
                       .label_result_example_heading_2, self.label_result_example_2]

        # ////////////////////// Buttons ///////////////////////////////

        self.btn_lookup = tk.Button(
            self.frame_left, text='Look Up', width=18, relief=tk.RAISED, command=self.lookup)
        self.btn_lookup.place(relx=0.10, rely=0.4)

        self.btn_openfile = tk.Button(
            self.frame_left, text='Open File', width=18, relief=tk.RAISED, command=self.open_file)
        self.btn_openfile.place(relx=0.10, rely=0.55)

        self.btn_History = tk.Button(
            self.frame_left, text='History', width=18, relief=tk.RAISED, command=self.history)
        self.btn_History.place(relx=0.10, rely=0.7)

        self.btn_open_location = tk.Button(
            self.frame_left, text='Open Folder', width=18, relief=tk.RAISED, command=self.open_location)
        self.btn_open_location.place(relx=0.10, rely=0.85)

        self.btn_view_more = tk.Button(
            self, text='View More', command=self.view_more)

        # ////////////////////// Menu Items ///////////////////////////////
        # ----------------------------------------------
        # Menu Items
        self.menu_bar = tk.Menu(self)

        # Menu item - File
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='New', command=self.open_new)
        self.file_menu.add_command(label='Open File', command=self.open_file)
        self.file_menu.add_command(label='History', command=self.history)
        self.file_menu.add_command(
            label='Open Folder', command=self.open_location)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Close', command=self.destroy)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        # Menu item - Help
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label='About', command=self.show_about)
        self.help_menu.add_command(label='Help', command=self.show_help)
        self.menu_bar.add_cascade(label='Help', menu=self.help_menu)

        self.configure(menu=self.menu_bar)

        # Menu item - Edit
        # self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        # self.edit_menu.add_command(label='Cut', command=self.cut_text)
        # self.edit_menu.add_command(label='Copy', command=self.copy_text)
        # self.edit_menu.add_command(label='Paste', command=self.paste_text)
        # self.edit_menu.add_command(label='Clear', command=self.clear_text_area)
        # self.menu_bar.add_cascade(label='Edit', menu=self.edit_menu)

        # ////////////////////// Functions ///////////////////////////////

    def reset_labels(self):

        for label in self.labels:
            label.configure(text="", bg="#fff")

    def lookup(self):
        self.reset_labels()
        self.definitions = []
        self.all_definitions = ""

        self.word = self.entry.get().lower()
        if not self.word:
            tkms.showinfo(
                "Blank Input", "Field is blank!! Please enter a proper word")
            self.entry.delete(0, 'end')
        elif not self.word.isalpha():
            tkms.showinfo(
                "Invalid Input", "The input consists of number , Please enter a proper word")
            self.entry.delete(0, 'end')
        else:
            start_time = time.perf_counter()

            self.fetch_definition(self.word)
            if self.error:
                self.label_status.configure(text="Invalid Input")
                self.label_info.configure(text="Word not found")
                self.error = False
                tkms.showinfo("Invalid Entry",
                              "Check the work and type again!!")
                self.entry.delete(0, 'end')
            else:

                if len(self.definitions) > 2:
                    self.btn_view_more.place(relx=0.85, rely=0.90)

                if len(self.definitions) <= 2:
                    self.label_info.configure(
                        text="Definitions Successfully loaded")
                    self.load_definitions()
                else:

                    self.label_info.configure(
                        text="More Definitions available, Click View More")
                    self.load_definitions()

                self.label_status.configure(
                    text=str(len(self.definitions)) + " Definition(s) found")

                self.search_history.append(self.word)  # record history

                end_time = time.perf_counter()

                self.time_taken = str(round(end_time - start_time, 2))
                self.label_load_time.configure(
                    text='Took ' + self.time_taken + "secs")

    def lookup_words(self):
        if not self.words_from_file:
            tkms.showinfo("Improper Words",
                          "No Valid words present in the file!!!")
        else:
            for word in self.words_from_file:
                self.fetch_definition(word)
        # print(self.words_definitions)

    def fetch_definition(self, word):
        self.definitions = []
        try:

            headers = {
                'Authorization': 'Token ' + open('key.txt').read(),
            }

            response = requests.get(
                'https://owlbot.info/api/v4/dictionary/' + word, headers=headers)

            # directly loads the response to a dictionary object in python
            result_dict = response.json()

            # print(result_dict.keys())

            if len(result_dict) > 1:
                for item in range(len(result_dict['definitions'])):
                    if result_dict['definitions'][item]["example"]:
                        definition = result_dict['definitions'][item][
                            "type"], result_dict['definitions'][item]["definition"], result_dict['definitions'][item]["example"]
                    else:
                        definition = result_dict['definitions'][item][
                            "type"], result_dict['definitions'][item]["definition"]

                    self.definitions.append(definition)

                self.words_definitions[word] = self.definitions

            else:
                self.error = True
                self.words_unfound.append(word)

        except requests.exceptions.ConnectionError:
            tkms.showinfo(
                "Connection Error", "There seems to be an issue with the network, Try later")
            self.label_status.configure(text="Network error")

    def load_definitions(self):

        self.label_result_type_heading.configure(text="Type")
        self.label_result_type.configure(
            text=self.definitions[0][0].capitalize())

        self.label_result_meanging_heading.configure(text="Meaning")
        self.label_result_meaning.configure(
            text=self.definitions[0][1].capitalize())
        if len(self.definitions[0]) > 2:
            self.label_result_example_heading.configure(text="Example")
            self.label_result_example.configure(
                text=self.definitions[0][2].capitalize())
        if len(self.definitions) > 1:
            self.label_result_type_heading_2.configure(text="Type")
            self.label_result_type_2.configure(
                text=self.definitions[1][0].capitalize())
            self.label_result_meanging_heading_2.configure(text="Meaning")
            self.label_result_meaning_2.configure(
                text=self.definitions[1][1].capitalize())
            if len(self.definitions[1]) > 2:
                self.label_result_example_heading_2.configure(text="Example")
                self.label_result_example_2.configure(
                    text=self.definitions[1][2].capitalize())

    def history(self):

        if not self.search_history:
            tkms.showinfo("No History items", "Search for few words first")
        else:

            history_app = History()
            # Looping through search words and creating labels for the same in a loop
            for index, item in enumerate(self.search_history, start=1):
                tk.Label(history_app, text=str(index) + ".  " + item.title(),
                         justify=tk.LEFT, font=("candara", 15, 'bold'), padx=40, pady=5).pack()

    def open_location(self):
        os.startfile(Path())

    def view_more(self):

        if not self.definitions:
            tkms.showinfo("No words Present", "Search for a word first")
        else:
            view_more_app = View_More()
            view_more_app.title(self.word)
            headings = ['Type', 'Definition', 'Example']
            for index, _ in enumerate(self.definitions):
                for i in range(len(self.definitions[index])):
                    self.all_definitions += headings[i] + ":  "
                    self.all_definitions += self.definitions[index][i]
                    self.all_definitions += "\n"
                    self.all_definitions += "\n"
                self.all_definitions += "----------------------------------------------------------------------"
                self.all_definitions += "\n"
            view_more_app.text.insert(INSERT, self.all_definitions)
            view_more_app.mainloop()

    def save_to_file(self):
        self.target_file_name = 'Definitions_' + self.file_name_with_ext
        self.target_file_dir = Path()  # current

        for word in self.words_definitions.keys():
            self.target_text += word
            self.target_text += "\n"
            self.target_text += "-" * len(word)
            self.target_text += "\n"

            # list contains multiple tuples
            for tuple_item in self.words_definitions[word]:
                self.target_text += "Type:  " + tuple_item[0]
                self.target_text += "\n"
                self.target_text += "Definition:  " + tuple_item[1]
                self.target_text += "\n"
                if len(tuple_item) > 2:
                    self.target_text += "Example:  " + tuple_item[2]
                    self.target_text += "\n"
                self.target_text += "-----------------------------------------------------------------------"
                self.target_text += "\n"
            self.target_text += "==============================================================================="
            self.target_text += "\n"
            self.target_text += "\n"

        self.user_result_response = False
        with open(self.target_file_name, 'w') as file:
            file.write(self.target_text)
        if not self.error:
            self.user_result_response = tkms.askyesno(
                "Success", "Do you want to see the result?")
        else:
            self.user_result_response = tkms.askyesno("One or Few Words not found", "Definitions saved to " + self.target_file_name +
                                                      " in the current directory, barring  word(s): " + ','.join(self.words_unfound) + " \n Open the result ?")

        if self.user_result_response:
            os.startfile(self.target_file_name)

    def open_file(self):
        self.reset_labels()
        self.entry.delete(0, 'end')
        self.words_unfound = []
        self.label_status.configure(text='Working')
        self.label_info.configure(text='Definitions are being fetched')
        path = tkfd.askopenfilename()
        if path:
            self.file_path = Path(path)
            self.file_name_with_ext = os.path.basename(self.file_path)
            self.file_name = self.file_name_with_ext.split(".")[0]
            self.file_extension = self.file_name_with_ext.split(".")[1]

            if self.file_extension == 'txt':
                with open(self.file_path) as file:
                    self.text_from_file = file.read()
                self.words_from_file = [item.strip()
                                        for item in self.text_from_file.split('\n')]
                start_time = time.perf_counter()
                self.lookup_words()
                end_time = time.perf_counter()
                self.time_taken = round(end_time - start_time, 2)
                self.label_load_time.configure(
                    text="Loaded in " + str(self.time_taken) + "secs")
                self.save_to_file()
            else:
                tkms.showwarning(
                    "Not Supported", "It only works with text files")

        # ////////////////////// Menu Items - Functions ///////////////////////////////

    def open_new(self):
        new_app = GUI()
        new_app.mainloop
        app.bind("<Return>", lambda x: app.lookup())
        app.bind("<Alt-F4>", lambda x: app.destroy())

    def show_about(self):
        tkms.showinfo(
            "DictVings V0.1", "Enjoy the First Version of the DictNotes. \n A small but practical Dictionary app \n\N{COPYRIGHT SIGN} Vings ")

    def show_help(self):
        user_visit_response = tkms.askyesno(
            "DictVings V0.1", "More information is available here https://hungry-edison-3a254b.netlify.app/ \n Do you want visit the site?")
        if user_visit_response:
            webbrowser.open_new(self.app_url)


if __name__ == '__main__':
    app = GUI()
    app.bind("<Return>", lambda x: app.lookup())
    app.bind("<Alt-F4>", lambda x: app.destroy())
    app.mainloop()
