
from pathlib import Path
import tkinter as tk
import tkinter.messagebox as tkms
from tkinter import messagebox
import time
import datetime
import re
import random
import os
import webbrowser
import threading
import multiprocessing
import logging
from playsound import playsound
import sounds
from cv2 import log

from matplotlib.ft2font import BOLD
from configparser import ConfigParser

import qa_query
import qa_injestion
import qa_update_flg
import pyperclip
import check_flgs
import qa_update_star

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s|%(levelname)s|%(name)s:-> %(message)s')
log_file = logging.FileHandler("VpyQuiz.log")
log_file.setFormatter(formatter)
logger.addHandler(log_file)

logger.info("########################################################################################################################")
logger.info("The application started")
logger.info("########################################################################################################################")


class GUI(tk.Tk):
    ########################################################################################################################
    # KEY VARIABLES
    ########################################################################################################################

    def __init__(self) -> None:
        super().__init__()
        self.window_height = "680"
        self.window_width = "1100"
        self.geometry(self.window_width + "x" + self.window_height)
        self.title("VPY-QUIZ")
        self.resizable(False, False)
        self.configure(bg='#141414')

        self.mode_selected = ''
        self.quiz_started = False
        self.no_of_questions = 0
        self.no_of_sessions = 0
        self.question_no = 0
        self.interval = 15
        self.revision_flg = 'Yes'  # both flgs are yes and no as their default values
        self.starred_flg = 'No'
        self.start_time = ''
        self.total_time = ''
        self.total_no_of_sessions = 1
        self.data = []
        self.is_answered = False
        self.is_paused = False
        self.is_stopped = False
        self.previous_data = []
        self.ids_list = []
        self.line_width = 50
        self.long_answer_len = 400
        self.table_selected = ''
        self.is_starred = False
        self.starred_qos = []
        self.retrieve_str_qos = False
        self.src_update_info = ''
        self.sound_alerts_status = True
        self.bg_music_status = False

        logger.info(f'An instance is creating and running!')
########################################################################################################################
# handling the closing event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
########################################################################################################################

# Styling
        # Main text area------------------
        # self.font_style_text = ("candara", 14)
        # self.text_area_bg = "#141414"
        # self.text_area_fg = "#fff"
        # self.text_area_cursor_color = "#fff"

        # # status bar and its items------------------
        # self.status_frame_bg = "#808080"
        # self.status_items_bg = "#fff"
        # self.status_items_fg = "#000"
        # self.status_items_font_style = ("Lucida sans", 10)
        self.font_style_text = ("candara", 14)
        self.font_style_text_L = ("candara", 13)
        self.font_style_text_M = ("candara", 11)
        self.font_style_text_S = ("candara", 10)
        self.font_style_text_info = ("Microsoft YaHei Light", 10)
        self.status_items_font_style = ("Yu Gothic", 10)

        # COLORS
        self.bg_grey_light = "#ADADAD"
        self.bg_grey_dark = "#141414"
        self.fg_blue = "#43dde6"
        self.fg_grey = "#f0f0f0"
        self.bg_button_organge = "#e88a1a"
        self.bg_button_brick = "#cf3030"

        self.text_area_bg = self.bg_grey_light
        self.status_frame_bg = self.bg_grey_dark
        self.status_items_bg = self.bg_grey_dark
        self.bg_frame_question = self.bg_grey_dark
        self.bg_frame_answer = self.bg_grey_light
        self.bg_frame_button = self.bg_grey_dark
        self.bg_buttons = self.bg_grey_dark

        self.text_area_fg = self.bg_grey_dark
        self.text_area_cursor_color = "#fff"
        self.status_items_fg = self.bg_grey_light
        self.fg_frame_question = self.bg_grey_dark
        self.fg_frame_answer = self.bg_grey_dark
        self.fg_frame_button = self.bg_grey_dark
        self.fg_buttons = self.bg_grey_light

        # status bar and its items------------------

        # ====================================================
########################################################################################################################


########################################################################################################################

# Menu Items
        self.menu_bar = tk.Menu(self)

        # Menu item - File
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='New', command=self.open_new)
        self.file_menu.add_command(
            label='Save_session', command=self.save_session)
        self.file_menu.add_command(label='Reset', command=self.reset_quiz)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        # Menu item - Edit
        self.select_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.select_menu.add_command(
            label='Select Mode', command=self.select_mode)
        self.select_menu.add_command(
            label='Select No of Questions', command=self.set_no_questions)
        self.select_menu.add_command(
            label='Get starred Questions', command=self.get_starred_questions)
        self.menu_bar.add_cascade(label='Select', menu=self.select_menu)

        self.star_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.star_menu.add_command(
            label='Star_Question', command=self.star_question)
        self.star_menu.add_command(
            label='Get_starred_Questions', command=self.get_starred_questions)
        self.menu_bar.add_cascade(label='Star', menu=self.star_menu)

        # Menu item - Tools
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.tools_menu.add_command(
            label='Open_page', command=self.open_full_page)
        self.tools_menu.add_command(
            label='Google_Question', command=self.google_question)
        self.tools_menu.add_command(
            label='Copy_Question', command=self.copy_question)
        self.tools_menu.add_command(
            label='Copy_Answer', command=self.copy_answer)
        self.menu_bar.add_cascade(label='Tools', menu=self.tools_menu)

        # Menu item - Subject
        self.subject_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.subject_menu.add_command(
            label='Python', command=self.select_sub_python)
        self.subject_menu.add_command(
            label='Pandas', command=self.select_sub_pandas)
        self.subject_menu.add_command(
            label='SQL', command=self.select_sub_sql)
        self.subject_menu.add_command(
            label='Etymology', command=self.select_sub_ety)

        self.menu_bar.add_cascade(label='Subject', menu=self.subject_menu)

        # Menu item - App Info
        self.info_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.info_menu.add_command(
            label='Get Recent Source Update', command=self.get_src_update)
        self.menu_bar.add_cascade(label='App Info', menu=self.info_menu)

        # Menu item - Bg Music
        self.bg_music_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.bg_music_menu.add_command(
            label='clock Ticking', command=self.select_bg_track_clock_ticking)
        self.bg_music_menu.add_command(
            label='Light Rain', command=self.select_bg_track_light_rain)
        self.bg_music_menu.add_command(
            label='Soft Rain', command=self.select_bg_track_soft_rain)
        self.bg_music_menu.add_command(
            label='Wind Chimes', command=self.select_bg_track_wind_chimes)
        self.bg_music_menu.add_command(
            label='Dramatic', command=self.select_bg_track_orchestra)
        self.bg_music_menu.add_command(
            label='Relaxing Waters', command=self.select_bg_track_relaxing_waters)
        self.bg_music_menu.add_command(
            label='Nature Sounds', command=self.select_bg_track_nature_sounds)
        self.menu_bar.add_cascade(label='Music', menu=self.bg_music_menu)

        # Menu item - Toggle Sound effects
        self.toggle_sound_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.toggle_sound_menu.add_command(label='Turn off BG', command=self.turn_bg_off)
        self.toggle_sound_menu.add_command(label='Turn Alerts OFF', command=self.turn_alrts_off)
        self.toggle_sound_menu.add_command(label='Turn Alerts ON', command=self.turn_alrts_on)
        self.menu_bar.add_cascade(label='Toggle Alerts', menu=self.toggle_sound_menu)

        # Menu item - Help
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label='About', command=self.show_about)
        self.help_menu.add_command(label='Help', command=self.show_help)
        self.menu_bar.add_cascade(label='Help', menu=self.help_menu)

        self.configure(menu=self.menu_bar)

    ########################################################################################################################
     # Status bar

        self.frame_status_bar = tk.Frame(
            self, width=self.window_width, height=24, bg=self.status_frame_bg, relief=tk.SUNKEN)
        self.frame_status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # ===============================================
        # Status items Below

        self.label_status = tk.Label(
            self.frame_status_bar, text='Ready', bg=self.status_items_bg, fg=self.status_items_fg, font=self.status_items_font_style, pady=-5)
        self.label_status.place(relx=0.005)

        self.label_day = tk.Label(self.frame_status_bar, text='Day', bg=self.status_items_bg,
                                  fg=self.status_items_fg, font=self.status_items_font_style, pady=-5)
        self.label_day.place(relx=0.77)

        self.label_date = tk.Label(self.frame_status_bar, text='Date', bg=self.status_items_bg,
                                   fg=self.status_items_fg, font=self.status_items_font_style, pady=-5)
        self.label_date.place(relx=0.87)

        self.label_time = tk.Label(
            self.frame_status_bar, text='Time', bg=self.status_items_bg, fg=self.status_items_fg, font=self.status_items_font_style, pady=-5)
        self.label_time.place(relx=0.45)

    ########################################################################################################################
    ########################################################################################################################
     # Status bar Above

        self.frame_status_bar_above = tk.Frame(
            self, width=self.window_width, height=17, bg=self.status_frame_bg, relief=tk.SUNKEN)
        self.frame_status_bar_above.pack(side=tk.TOP, fill=tk.X)

        # ===============================================
        # Status items

        self.label_qustion_no = tk.Label(
            self.frame_status_bar_above, text='Question No', bg=self.status_items_bg, fg=self.status_items_fg, font=self.status_items_font_style, pady=-5)
        self.label_qustion_no.place(relx=0.005)

        self.label_qustion_no_value = tk.Label(
            self.frame_status_bar_above, text='', bg=self.status_items_bg, fg=self.fg_blue, font=self.status_items_font_style, pady=-5)
        self.label_qustion_no_value.place(relx=0.1)

        self.label_title = tk.Label(self.frame_status_bar_above, text='Vpy - Flash | Revise & Retain', bg=self.status_items_bg,
                                    fg=self.fg_blue, font=self.status_items_font_style, pady=-5)
        self.label_title.place(relx=0.40)

        self.label_time_taken = tk.Label(self.frame_status_bar_above, text='Time Taken for this Session', bg=self.status_items_bg,
                                         fg=self.status_items_fg, font=self.status_items_font_style, pady=-5)
        self.label_time_taken.place(relx=0.75)

        self.label_time_taken_value = tk.Label(self.frame_status_bar_above, text='', bg=self.status_items_bg,
                                               fg=self.fg_blue, font=self.status_items_font_style, pady=-5)
        self.label_time_taken_value.place(relx=0.92)

        ########################################################################################################################

        # ////////////////////////////////// Frames ////////////////////////////////////////////

        self.frame_question = tk.Frame(
            self, width=1070, height=220, bg=self.bg_frame_question)
        self.frame_question.place(relx=0.005, rely=0.05)

        self.frame_answer = tk.Frame(
            self, width=1070, height=290, bg=self.bg_frame_answer)
        self.frame_answer.place(relx=0.005, rely=0.382)

        self.frame_buttons = tk.Frame(
            self, width=self.window_width, height=90,  bg=self.bg_frame_button)
        self.frame_buttons.place(relx=0, rely=0.82)

        # ////////////////////////////////// Question frame ////////////////////////////////////////////

        self.label_qustion_frame = tk.Label(
            self.frame_question, text='Type the Question: ', bg=self.status_items_bg, fg=self.status_items_fg, font=self.status_items_font_style, pady=-5)
        self.label_qustion_frame.place(relx=0.01, rely=0.02)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area = tk.Text(
            self.frame_question, bg=self.text_area_bg, font=self.font_style_text, fg=self.text_area_fg,
            width=90, height=150, insertbackground=self.text_area_cursor_color, yscrollcommand=self.scrollbar.set, undo=True, insertwidth=0.5, selectbackground="#000000")
        self.text_area.place(relx=0.1, rely=0.135)
        self.scrollbar.config(command=self.text_area.yview)
        # self.scrollbar.config(command=self.text_area.yview)

        # ////////////////////////////////// Answer frame ////////////////////////////////////////////

        self.label_answer_frame_title = tk.Label(
            self.frame_answer, text='Explanation: ', bg=self.status_items_bg, fg=self.status_items_fg, font=self.status_items_font_style, pady=-5)
        self.label_answer_frame_title.place(relx=0.01, rely=0.02)

        self.label_answer_frame = tk.Label(
            self.frame_answer, width=130,  wraplength=780, height=15, text='', justify=tk.LEFT,
            bg=self.status_items_bg, fg=self.status_items_fg, font=self.font_style_text_M, pady=-5)
        self.label_answer_frame.place(relx=0.1, rely=0.135)

        # ////////////////////////////////// Buttons ////////////////////////////////////////////

        self.b_width = 12
        self.b_height = 5
        self.b_style = 'raised'

        self.button_mode = tk.Button(
            self.frame_buttons, text='MODE', width=self.b_width, height=self.b_height, relief=self.b_style, font=self.font_style_text_S, command=self.select_mode, bg=self.bg_buttons, fg=self.fg_buttons)
        self.button_mode.place(relx=0.002, rely=0.021)

        self.button_no_of_questions = tk.Button(
            self.frame_buttons, text='Questions \n Per \n  Session', width=self.b_width, height=self.b_height, relief=self.b_style, font=self.font_style_text_S, command=self.set_no_questions, bg=self.bg_buttons, fg=self.fg_buttons)
        self.button_no_of_questions.place(relx=0.0885, rely=0.021)

        self.button_show_answer = tk.Button(
            self.frame_buttons, text='Answer', width=self.b_width, height=self.b_height, relief=self.b_style, font=self.font_style_text_S, command=self.show_answer, bg=self.bg_buttons, fg=self.fg_buttons)
        self.button_show_answer.place(relx=0.175, rely=0.021)

        self.button_start = tk.Button(
            self.frame_buttons, text='Start', width=self.b_width, height=self.b_height, relief=self.b_style, font=self.font_style_text_S, command=self.start_session, bg=self.bg_buttons, fg=self.fg_buttons)
        self.button_start.place(relx=0.643, rely=0.021)

        self.button_stop = tk.Button(
            self.frame_buttons, text='Restart', width=self.b_width, height=self.b_height, relief=self.b_style, font=self.font_style_text_S, command=self.restart_session, bg=self.bg_buttons, fg=self.fg_buttons)
        self.button_stop.place(relx=0.729, rely=0.021)

        self.button_reset = tk.Button(
            self.frame_buttons, text='Reset', width=self.b_width, height=self.b_height, relief=self.b_style, font=self.font_style_text_S, command=self.reset_quiz, bg=self.bg_buttons, fg=self.fg_buttons)
        self.button_reset.place(relx=0.815, rely=0.021)

        self.button_next = tk.Button(
            self.frame_buttons, text='Next', width=self.b_width, height=self.b_height, relief=self.b_style, font=self.font_style_text_S, command=self.next_question, bg=self.bg_buttons, fg=self.fg_buttons)
        self.button_next.place(relx=0.9, rely=0.021)

        self.label_info_title = tk.Label(
            self.frame_buttons, text='Inforamation Panel: ', bg=self.status_items_bg, fg=self.fg_blue,
            font=self.font_style_text_L, pady=-5, justify=tk.CENTER)
        self.label_info_title.place(relx=0.275, rely=0.021)

        self.label_info = tk.Label(
            self.frame_buttons, text='Select Mode and No of Questions to start with!', bg=self.status_items_bg, fg=self.fg_grey,
            font=self.font_style_text_info)
        self.label_info.place(relx=0.33, rely=0.28)

    ########################################################################################################################
    # Code for status items such time,day etc.,
    ########################################################################################################################

        today = datetime.datetime.today()
        day_int = today.weekday()  # Monday starts at 0
        week_days = {idx: day for idx, day in enumerate(
            ["Monday", "Tuesday", "Wednsday", "Thursday", "Friday", "Saturday", "Sunday"])}
        self.label_day.configure(text=(week_days[day_int]))

        self.show_time()

        self.label_date.configure(text=datetime.datetime.now().date())

        ########################################################################################################################
        # The following are working fine! but didn't want to use
        # canvas to draw the line under the information panal
        self.canvas = tk.Canvas(
            self, width=390, height=1, bg='#808080')
        self.canvas.place(relx=0.27, rely=0.95)
        self.bk_canvas = tk.Canvas(
            self, width=40, height=40, bg=self.bg_grey_dark, highlightthickness=0)
        self.bk_canvas.place(relx=0.02, rely=0.17)
    #     self.line_y1 = 0
    # #     self.line_y2 = 1

    #     self.canvas_ticker = tk.Canvas(
    #         self, width=360, height=10, bg='#d9d9d9')
    #     self.canvas_ticker.place(relx=0.055, rely=0.97)
    #     self.ticker_text = 'PYQUIZ'

    # # def animate_line(self):
    # #     if self.line_y1 <= 390:
    # #         self.canvas.create_line(
    # #             0, 0, self.line_y1, self.line_y2, width=50, fill='#000')
    # #         self.line_y1 += 5
    # #         # self.line_y2 += 10

    # #     else:
    # #         self.line_y1 = 0
    # #         # self.line_y2 = 0
    # #         self.canvas.delete('all')
    # #     self.canvas.after(200, self.animate_line)

    # def animate_text(self):
    #     self.canvas_ticker.delete('all')
    #     if self.line_y1 <= 360:
    #         self.canvas_ticker.create_text(self.line_y1, 6, text=self.ticker_text,
    #                                        font=("Helvetica", 9),tag = 'text',
    #                                        fill="grey")
    #         self.line_y1 += 2
    #         # self.line_y2 += 10

    #     else:
    #         self.line_y1 = 0
    #         # self.line_y2 = 0
    #         self.canvas.delete('all')
    #     self.canvas.after(100, self.animate_text)

    def create_bookmark(self):
        self.bk_canvas.create_oval(10, 10, 40, 40,
                                   fill=self.fg_blue,
                                   )

    ########################################################################################################################
        # functions_staging_area
    ########################################################################################################################

    def select_mode(self):
        if not self.quiz_started:
            logger.info(f'The quiz has not started Yet!')
            logger.info(f'mode selection class is called')
            mode_window_app = mode_window()
            mode_window_app.mainloop()

    def set_no_questions(self):
        if not self.quiz_started:
            logger.info(f'The quiz has not started Yet!')
            logger.info(f'no of questions class is called')
            q_nos_app = Q_nos_app()
            q_nos_app.mainloop()

    def select_sub_python(self):
        if not self.quiz_started:
            self.table_selected = 'PYTHON_DATA'
            self.pass_info("Learn and Revise the Python Questions!")

    def select_sub_pandas(self):
        if not self.quiz_started:
            self.table_selected = 'PANDAS_DATA'
            self.pass_info("Learn and Revise the Pandas Questions!")

    def select_sub_sql(self):
        if not self.quiz_started:
            self.table_selected = 'SQL_DATA'
            self.pass_info("Learn and Revise the SQL Questions!")

    def select_sub_ety(self):
        if not self.quiz_started:
            self.table_selected = 'ETYMOLOGICAL_REFERENCES'
            self.pass_info("Learn and Revise the Questions from etymology!")

    def get_starred_questions(self):
        self.starred_flg = 'Yes'
        self.pass_info("Now, only the starred questions will come up")

    def start_session(self):
        # setting up the default values in case thostatusse buttons are not used
        if not self.mode_selected:
            logger.info(f'No Mode is selected;')
            logger.info(f'Setting the mode to the Default value: REVISION')
        if not self.no_of_questions:
            logger.info(f'No of questions are not selected;')
            logger.info(f'Setting the no of questions to  Default value: 3')
        if not self.table_selected:
            logger.info(f'No Subject is selected')
            logger.info(f'The Default subject is selected : Python')

        self.mode_selected = 'REVISION' if not self.mode_selected else self.mode_selected
        self.no_of_questions = 3 if not self.no_of_questions else self.no_of_questions
        self.table_selected = 'PYTHON_DATA' if not self.table_selected else self.table_selected

        logger.info(f'Start button in clicked')
        logger.info(f'the operational mode is {self.mode_selected}')

        self.button_mode.configure(text=self.mode_selected)
        self.button_no_of_questions.configure(
            text=self.no_of_questions)
        self.data_imported = ()

        if self.is_stopped:
            self.data = self.previous_data
            logger.info(
                f'The data has been temporarily saved to restart the session!')
            self.button_stop.configure(text='Restart')
            self.button_next.configure(state='normal')
            self.button_show_answer.configure(state='normal')
            self.label_status.configure(text='Restarted!')

        elif self.mode_selected == 'RANDOM':
            self.revision_flg = 'No'
            random_avl_check = check_flgs.get_status(
                self.no_of_questions, self.table_selected, 'RANDOM_CHECK')
            if not random_avl_check[0]:
                self.pass_info(
                    f"Not enough random questions available. \n  (only {random_avl_check[1]} available for learning)")
                logger.info(
                    f"Not enough random questions available. \n  (only {random_avl_check[1]} available for learning)")
                self.start_sound_thread('Buzz')
            else:
                self.data_imported = qa_query.get_questions(
                    self.no_of_questions, self.revision_flg, self.table_selected)  # get the questions randomly selected from the database
                self.data = self.data_imported[0]
                self.ids_list = self.data_imported[1]
                logger.info(
                    f'Since the selected is RANDOM, new data has been populated from the db: {self.table_selected} and the ids thereof have been saved.')
                self.activate_start_mode()

        elif self.mode_selected == 'REVISION':
            revison_summary = check_flgs.get_status(
                self.no_of_questions, self.table_selected, 'REVISION_CHECK')
            if not revison_summary[0]:
                self.pass_info(
                    f"Not enough revision questions available. \n  (only {revison_summary[1]} available for revision)")
                logger.info(
                    f"Not enough revision questions available. \n  (only {revison_summary[1]} available for revision)")
            elif self.revision_flg == 'Yes' and self.starred_flg == 'Yes':
                starred_summary = check_flgs.get_status(
                    self.no_of_questions, self.table_selected, 'STAR_CHECK')
                if not starred_summary[0]:
                    self.pass_info(
                        f"Not enough starred questions available. \n  (only {starred_summary[1]} are starred so far)")
                    logger.info(
                        f"Not enough starred questions available. \n  (only {starred_summary[1]} are starred so far)")
                    self.start_sound_thread('Buzz')
                else:
                    self.data_imported = qa_query.get_questions(
                        self.no_of_questions, self.revision_flg, self.table_selected, self.starred_flg)  # get the questions tagged as 'yes' for revision
                    self.data = self.data_imported[0]
                    self.ids_list = self.data_imported[1]
                    logger.info(
                        f'Since the mode selected is REVISION, the corresponding data has been called')
                    self.activate_start_mode()
            else:
                self.revision_flg = 'Yes'
                self.data_imported = qa_query.get_questions(
                    self.no_of_questions, self.revision_flg, self.table_selected)  # get the questions tagged as 'yes' for revision
                self.data = self.data_imported[0]
                self.ids_list = self.data_imported[1]
                logger.info(
                    f'Since the mode selected is REVISION, the corresponding data has been called')
                self.activate_start_mode()

    def activate_start_mode(self):
        self.quiz_started = True
        self.start_time = datetime.datetime.now()
        self.is_answered = False
        self.label_status.configure(text='Started', fg='#808080')
        self.is_stopped = False

        self.label_info.configure(
            text="The quiz has begun. Good Luck!")
        self.label_qustion_no_value.configure(
            text=f'1 of {self.no_of_questions}')

        self.question_no = 1
        self.text_area.configure(state='normal')
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert("1.0", self.data[0][0])
        self.text_area.configure(state='disabled')
        self.button_start.configure(text='Started', state='disabled')
        logger.info(f'The Quiz has started!')
        logger.info(f'Question no {self.question_no} is running!')
        self.start_timer()
        # Change button colors
        self.button_mode.configure(bg=self.bg_button_organge, fg='#000')
        self.button_no_of_questions.configure(
            bg=self.bg_button_organge, fg='#000')
        self.button_start.configure(bg=self.bg_button_organge, fg='#000')

        logger.info(f'The timer has been started!')
        self.start_sound_thread('Start')

    def open_new(self):
        new_app = GUI()
        new_app.mainloop()

    def show_answer(self):
        if self.quiz_started and self.question_no <= self.no_of_questions:
            self.answer = self.data[self.question_no - 1][1]
            if len(self.answer) > self.long_answer_len:
                self.pass_info(
                    f' Open Tools and then Open_page  to see \n the full explanation in a new window!')
                # self.start_sound_thread('open_page')

            self.label_answer_frame.configure(text=self.answer)
            logger.info(
                f'The answer to the question no {self.question_no} is shown')
            self.is_answered = True
            if self.question_no == self.no_of_questions:
                self.pass_info(
                    "That's Good one! \n Click on the NEXT to Continue")
        if not self.quiz_started or not self.question_no:
            self.pass_info(text="Please start the Quiz First!")
            logger.info(
                f'User clicked on the ANSWER without starting the quiz!')
            self.start_sound_thread('Buzz')

    def next_question(self):
        if self.quiz_started and self.question_no < self.no_of_questions and self.is_answered:
            self.start_sound_thread('Next')
            self.label_answer_frame.configure(text='')
            self.text_area.configure(state='normal')
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert("1.0", self.data[self.question_no][0])
            self.text_area.configure(state='disabled')
            self.question_no += 1
            self.label_qustion_no_value.configure(
                text=f'{self.question_no} of {self.no_of_questions}')
            if (self.no_of_questions - self.question_no) == 0:
                self.pass_info("This is the last Question!")
            elif (self.no_of_questions - self.question_no) == 1:
                self.pass_info("Just a question more to go!")
            else:
                self.pass_info(
                    f'{self.no_of_questions - self.question_no} Questions are remaining')

            self.is_answered = False
            logger.info(f'NEXT button is pressed')
            logger.info(f'Question no {self.question_no} is shown now')
            if self.is_starred:
                self.bk_canvas.delete('all')

        elif not self.question_no:
            self.pass_info(
                text="Please start the Quiz to move to the next Question!")
            logger.info(f'User tried to click next without starting the quiz')
            self.start_sound_thread('Buzz')

        # when the last question is reached to
        elif self.question_no == self.no_of_questions and self.is_answered:
            self.text_area.configure(state='normal')
            self.text_area.delete('1.0', tk.END)
            self.text_area.configure(state='disabled')
            logger.info(f'{self.revision_flg} -- revision flag')
            if self.revision_flg == 'No':
                qa_update_flg.update_revision_flg(
                    self.ids_list, self.table_selected)
                logger.info(
                    f'The db: {self.table_selected} is updated with the revision flags successfully!')
            else:
                logger.info(
                    f'db: {self.table_selected} is not updated with the revision flag as the selected mode was REVISION')

            if self.is_starred:
                print(self.starred_qos)
                print(self.table_selected)
                self.bk_canvas.delete('all')
                qa_update_star.update_star_flg(
                    self.starred_qos, self.table_selected)
                logger.info(
                    f'Questions ids {self.starred_qos} have been updated with Starred flag in {self.table_selected} table')

            self.button_mode.configure(bg=self.bg_buttons, fg=self.fg_buttons)
            self.button_no_of_questions.configure(
                bg=self.bg_buttons, fg=self.fg_buttons)
            self.button_start.configure(bg=self.bg_buttons, fg=self.fg_buttons)
            time_taken = self.count_time()
            self.reset_quiz()
            self.start_sound_thread('Start')  # same tone as start
            logger.info(f'The quiz has been reset successfully!')
            logger.info(
                f'User successfully completed the session no {self.total_no_of_sessions}')
            self.pass_info(
                text=f"Session Complete! \n Please start again! \n That was Session: {self.total_no_of_sessions} and it took {time_taken} secs")
            self.total_no_of_sessions += 1

        elif not self.is_answered:
            self.pass_info("The question must be answered before proceeding!")
            logger.info(
                f'User tried to click on the next without answering the question')
            self.start_sound_thread('Buzz')

    def restart_session(self):
        if self.quiz_started and not self.is_stopped:
            warning = tkms.showwarning(
                title='Restart the Session?', message='Do you want to restart the same session from the beginning?')
            if warning:
                self.button_stop.configure(text='Restarted')
                self.label_status.configure(text='Restarted')
                self.previous_data = self.data.copy()
                self.reset_quiz()
                logger.info(f'The session is restarted!')

                # Deactiving All the buttons
                self.button_next.configure(state='disabled')
                self.button_show_answer.configure(state='disabled')

                # self.label_time_taken_value.configure(text=self.time_elapsed)
                self.button_start.configure(text='Start Again', state='normal')
                self.is_stopped = True
        elif not self.quiz_started:
            self.pass_info("You can't restart without starting a session!")
            self.start_sound_thread('Buzz')

    def clear_canvas(self):
        self.label_answer_frame.configure(text='')
        self.label_qustion_no_value.configure(text='')
        self.label_time_taken_value.configure(text='')
        self.text_area.configure(state='normal')
        self.text_area.delete('1.0', tk.END)
        self.pass_info('')
        self.button_mode.configure(bg=self.bg_buttons, fg=self.fg_buttons)
        self.button_no_of_questions.configure(
            bg=self.bg_buttons, fg=self.fg_buttons)
        self.button_start.configure(bg=self.bg_buttons, fg=self.fg_buttons)
        if self.is_starred:
            self.bk_canvas.delete('all')

    def count_time(self):
        present_time = datetime.datetime.now()
        time_taken = present_time - self.start_time
        # extracting only the reuqiered portion of the elapsed
        time_taken = str(self.time_elapsed)[:7]
        return time_taken

    def reset_quiz(self):
        if self.quiz_started:
            self.label_answer_frame.configure(text='')
            self.text_area.delete('1.0', tk.END)
            self.button_start.configure(text='Start', state='normal')
            self.label_status.configure(text='Reset')
            self.mode_selected = ''
            self.table_selected = ''
            self.quiz_started = False
            self.no_of_questions = 0
            self.no_of_sessions = 0
            self.question_no = 0
            self.revision_flg = ''
            self.start_time = ''
            self.total_time = ''
            self.data = ''
            self.is_answered = False
            self.is_paused = False
            self.is_stopped = False

            self.clear_canvas()
            # tkms.showinfo(
            #     "The Quiz has been reset!", "Have a wonderful time now!")
        else:
            self.pass_info("Quiz can't be reset wtihout starting!")
            self.start_sound_thread('Buzz')

    def copy_question(self):
        if self.quiz_started:
            pyperclip.copy(self.data[self.question_no-1][0])
            text = f'Question no : {self.question_no} has been copied to clipboard!'
            logger.info(text)
            self.pass_info(text)
        else:
            self.pass_info("Start the quiz!, First")
            self.start_sound_thread('Buzz')

    def copy_answer(self):
        if self.quiz_started and self.is_answered:
            pyperclip.copy(self.answer)
            text = f'Answer for the Question no : {self.question_no} \n has been copied to clipboard!'
            logger.info(text)
            self.pass_info(text)
        else:
            self.pass_info("Answer is not yet available to Copy!")
            self.start_sound_thread('Buzz')

    def star_question(self):
        if self.quiz_started:
            self.create_bookmark()
            self.is_starred = True
            if self.starred_qos and self.starred_qos[-1] == self.ids_list[self.question_no-1]:
                self.pass_info(
                    f'The question has already been starred! \n Please Proceed!')
                self.start_sound_thread('Buzz')
            else:
                self.starred_qos.append(self.ids_list[self.question_no-1])
                self.pass_info(f'The question has been starred!')
                logger.info(
                    f'Questions with ids: {self.starred_qos} have been starred')

    def google_question(self):
        if self.quiz_started:
            # skipping 'Q.' since it is opened in a browser
            google_dom = "https://www.google.com/search?q="
            url = google_dom + self.data[self.question_no-1][0][2:]
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(
                "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"))
            webbrowser.get('chrome').open(url)
            logger.info(
                f'Question no {self.question_no} has been searched on google')
        else:
            self.pass_info("There is no question available to google!")
            self.start_sound_thread('Buzz')

    def open_full_page(self):
        if self.quiz_started:
            if self.is_answered:
                logger.info(
                    f'Page_Reader class has been called for question no: {self.question_no} ')
                page_app = Page_Reader(self.answer)
                page_app.mainloop()
            else:
                self.pass_info(
                    "The Answer must be shown to be able \n to open in new page")
        else:
            self.pass_info(f'The Quiz has not yet Started!')
            self.start_sound_thread('Buzz')

    def get_src_update(self):
        text = self.src_update_info
        tkms.showinfo('Source Update Information', text)
        self.start_sound_thread('Buzz')

    def show_about(self):
        tkms.showinfo("VPython.quiz 1.0",
                      "A Simple flash questions application for python!")
        logger.info(f'Show About is opened')

    def show_help(self):
        tkms.showinfo("Help!", "Select the Mode and Start Playing! \n Random   : To select questions Randomly \n Revision   : To Revise the already visited questions \n Look up   : To Search for questions  ")
        logger.info(f'Show Help is opened')

    def save_session(self):
        if self.quiz_started:
            today_date = datetime.datetime.today()
            title = "Saved_session_" + \
                str(today_date)[:10] + "_" + str(today_date)[11:19] + ".txt"
            title = title.replace(":", "_")
            with open(title, 'a') as file:
                for item in self.data:
                    for part in item:
                        file.write(part)
                        file.write("\n")
                    file.write(
                        "==================================================================")
                    file.write("\n")
            tkms.showinfo("FIle Saved Successfully!",
                          f"The Session has been saved as {title} in the current directory")
            logger.info(
                f'The session has been saved  to a local file : {title}')
        else:
            self.pass_info('No Session is available to save!')
            self.start_sound_thread('Buzz')

    def pass_info(self, text):
        self.label_info.configure(text=text)


########################################################################################################################
# Background Music Seciton
    def select_bg_track_clock_ticking(self):
        self.bg_music_status = 'True'
        self.start_sound_thread('clock_ticking')

    def select_bg_track_light_rain(self):
        self.bg_music_status = 'True'
        self.start_sound_thread('light_rain')

    def select_bg_track_soft_rain(self):
        self.bg_music_status = 'True'
        self.start_sound_thread('soft_rain')

    def select_bg_track_wind_chimes(self):
        self.bg_music_status = 'True'
        self.start_sound_thread('wind_chimes')

    def select_bg_track_orchestra(self):
        self.bg_music_status = 'True'
        self.start_sound_thread('orchestra')

    def select_bg_track_relaxing_waters(self):
        self.start_sound_thread('relaxing_waters')

    def select_bg_track_nature_sounds(self):
        self.bg_music_status = 'True'
        self.start_sound_thread('nature_sounds')

    def turn_bg_off(self):
        self.bg_music_status = False # tihs won't work anyway the individual flags above overwrite this

    def turn_alrts_off(self):
        self.sound_alerts_status = False
        self.pass_info(f'There will be No Sound Alerts')

    def turn_alrts_on(self):
        self.sound_alerts_status = True
        self.pass_info(f'Sound Alerts are Back..')
        



########################################################################################################################

        
    def start_sound_thread(self,label):
        if self.bg_music_status or self.sound_alerts_status:
                threading.Thread(target=self.play_sound,args = [label]).start()

                if len(label) > 5: # so the alerts names should always be less than 5
                    self.bg_music_status = False

    def play_sound(self,label):
        # sounds is a seperate python module with just the names and locations of the sounds
            sound_effect = sounds.select_sounds[label]
            playsound(sound_effect)


    def start_timer(self):
        if self.quiz_started:
            current_time = datetime.datetime.now()
            self.time_elapsed = current_time - self.start_time
            # extracting only the reuqiered portion of the elapsed
            self.time_elapsed = str(self.time_elapsed)[:7]
            self.label_time_taken_value.configure(text=self.time_elapsed)
            self.label_time_taken_value.after(200, self.start_timer)
########################################################################################################################
# Functions for Status Items
########################################################################################################################

    def show_time(self):
        self.time = time.strftime("%H:%M:%S")
        self.label_time.configure(text=self.time)
        self.label_time.after(200, self.show_time)

    def on_closing(self):
        if self.quiz_started:
            if messagebox.askokcancel("Quit", "Looks like you are in the middle of the quiz? \n\n  Do you really want to quit?"):
                logger.info(f'The application is closing down!')
                self.destroy()
        else:
            if messagebox.askokcancel("Quit", "That's good stop! \n\n Do you want to leave for now?"):
                logger.info(f'The application is closing down!')
                self.destroy()


app = GUI()


class mode_window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.window_height = "200"
        self.window_width = "300"
        self.geometry(self.window_width + "x" + self.window_height)
        self.title("Select the Mode")
        self.resizable(False, False)
        self.geometry('+420+280')
        # if we won't mention 'self' it is not going to return anything, we won't be able
        self.var = tk.StringVar(self)
        # to read from the radiobuttons

        self.radio_button_top = tk.Radiobutton(self, text="RANDOM", variable=self.var, value='RANDOM',
                                               command=self.get_status)
        self.radio_button_top.place(relx=0.35, rely=0.2)
        self.radio_button_middle = tk.Radiobutton(self, text="REVISION", variable=self.var, value='REVISION',
                                                  command=self.get_status)
        self.radio_button_middle.place(relx=0.35, rely=0.4)
        self.radio_button_bottom = tk.Radiobutton(self, text="LOOK UP", variable=self.var, value='LOOK UP',
                                                  command=self.get_status)
        self.radio_button_bottom.place(relx=0.35, rely=0.6)

        self.button_ok = tk.Button(
            self, width=28, height=2,  bg="#A1A5A6", text='Okay', command=self.start)
        self.button_ok.place(relx=0.12, rely=0.76)

    def get_status(self):
        self.status = str(self.var.get())
        # GUI.mode_selectd = self.status
        # Changes the values across the classes
        setattr(app, "mode_selected", self.status)
        app.pass_info(f'{self.status} mode is selected')
        logger.info(f'from the mode window: {self.status} mode is  seleced ')
        logger.info(
            f'from the mode window: {self.status} mode is  passed to an instance - app')
        # the first param in the setattr() is app not GUI (the main class) because if we chagne the attribte of the main class
        # it will only be avaialbe while constrction(first time) to the instances, but the subsequest changes will not be
        #  availble to the instances of the class
        # Hence we created an instance and them passing / changing the attributes there of

    def start(self):
        self.destroy()


class Q_nos_app(tk.Tk):
    def __init__(self):
        super().__init__()
        self.window_height = "200"
        self.window_width = "300"
        self.geometry(self.window_width + "x" + self.window_height)
        self.title("Select a Number")
        self.resizable(False, False)
        self.geometry('+420+280')
        self.label = tk.Label(self)
        self.label.place(relx=0.25, rely=0.25)
        self.default_no_of_questions = 3

        self.slider = tk.Scale(self, from_=2, to=10,
                               orient=tk.HORIZONTAL)
        # bg=self.bg_widgets, fg=self.fg_widgets)
        self.slider.place(relx=0.30, rely=0.45)
        self.slider.set(self.default_no_of_questions)

        self.button = tk.Button(self, width=20, height=1,
                                text='SELECT', command=self.show_time_hints)
        self.button.place(relx=0.26, rely=0.75)

        # self.button_min = tk.Button(self, width=8, height=3,
        #                         text='Set MIN', command=self.slider.configure(set = 2))
        # self.button_min.place(relx=0.15, rely=0.25)

        # self.button_max = tk.Button(self, width=8, height=3,
        #                         text='Set MAX', command=self.slider.set(10))
        # self.button_max.place(relx=0.65, rely=0.25)
        self.is_button_clicked = False
        self.last_selected_value = ''

    def show_time_hints(self):
        self.selected_qos = self.slider.get()
        if not self.is_button_clicked or self.last_selected_value != self.selected_qos:
            if not self.selected_qos:
                self.label_text = f"Please select a valid no of Questions!"
            else:
                self.label_text = f"That is {self.selected_qos * 15 / 60} Min per this session \n ({self.selected_qos} Questions x 15 secs)"
            self.label.configure(text=self.label_text)
            self.button.configure(text='Confirm (Or) ReSelect')
            self.is_button_clicked = True
            self.last_selected_value = self.selected_qos
        elif self.is_button_clicked and self.last_selected_value == self.selected_qos and self.selected_qos:
            logger.info(
                f'From the no of questions window: {self.selected_qos} questions have been selected')
            setattr(app, "no_of_questions", self.selected_qos)
            app.pass_info(f'{self.selected_qos} questions have been selected')
            logger.info(
                f'From the no of questions window: {self.selected_qos} questions have been passed to an instance - app')
            self.destroy()


class Page_Reader(tk.Tk):
    def __init__(self, page_content):
        super().__init__()
        self.window_height = "680"
        self.window_width = "570"
        self.geometry(self.window_width + "x" + self.window_height)
        self.title("Select a Number")
        self.resizable(False, False)
        self.geometry('+400+10')
        self.configure(bg='#ABABAB')
        self.page_content = page_content
        self.status_items_font_style = ("Yu Gothic", 10)

        self.text = tk.Label(
            self, text=self.page_content, bg='#141414', fg='#fff', font=("candara", 11), justify=tk.LEFT, wraplength=500, padx=5, pady=5)
        self.text.place(relx=0.06, rely=0.10)

        self.button_close = tk.Button(
            self, text='Close & Continue', bg='#A3F4C3', command=self.close_window, width=30, height=3)
        self.button_close.place(relx=0.31, rely=0.8)
        logger.info(f'New page / window is opened for the full explanation')

    def close_window(self):
        self.destroy()


if __name__ == '__main__':

    def check_sources():
        logger.info(f'Checking for the sources data update...')
        config_reader = ConfigParser()
        config_reader.read("DB_Data/sources.ini")
        source = config_reader['sources']
        sources = {table: timpstp for table,
                   timpstp in source.items()}
        sources_prev_time = [src for src in sources.values()]
        sources_paths = [r"I:\Do\Vings\python__\projects\Advanced\VPython_Quiz\VPython - Quiz 2.0\Data.txt",
                         r"I:\Do\Vings\python__\projects\Advanced\VPython_Quiz\VPython - Quiz 2.0\Pandas_data.txt",
                         r"I:\Do\Vings\python__\projects\Advanced\VPython_Quiz\VPython - Quiz 2.0\Etymology.txt"]
        latest_timpstms = [str(os.path.getmtime(path))
                           for path in sources_paths]
        sources_latest_time = {key: value for key, value in zip(
            sources, latest_timpstms)}  # zip also works with dict, just takes their keys
        logger.info(f'Previous Time Stamps {sources}')
        logger.info(f'Latest Time Stamps {sources_latest_time}')

        not_mathcing_tmpstmp = [i for i, j in zip(
            sources_prev_time, latest_timpstms) if i != j]

        tables_to_be_updated = []
        for table, tmstp in sources.items():
            for mismatch in not_mathcing_tmpstmp:
                if tmstp == mismatch:
                    tables_to_be_updated.append(table)
        if not tables_to_be_updated:
            logger.info(f'No recent update for any of the tables found')
            setattr(app, 'src_update_info',
                    f'No recent update for any of the tables found')
            logger.info(f'Calling the main Applicaition w/o any source update')
            app.mainloop()
        else:
            logger.info(
                f'Table(s) : {tables_to_be_updated} are udpated recently')
            new_recs = qa_injestion.get_updated_recs(tables_to_be_updated)
            if new_recs[1]:
                setattr(app, 'src_update_info', new_recs[0])
                logger.info(
                    f'{new_recs[0]}')
                logger.info(
                    f'Data Injestion is successful with {new_recs[1]} record(s)')
            else:
                text = f'No New Records but the data has been udpated Successfully for tables: {tables_to_be_updated}'
                logger.info(text)
                setattr(app, 'src_update_info', text)
            for table, tmstp in sources_latest_time.items():
                if table in tables_to_be_updated:
                    source[table] = tmstp
            with open("DB_Data/sources.ini", 'w') as conf:
                config_reader.write(conf)
            logger.info(
                f'Latest Time Stamps have been udpated for tables : {tables_to_be_updated}')
            logger.info(f'Calling the main Applicaition After the update')
            app.mainloop()

    check_sources()
