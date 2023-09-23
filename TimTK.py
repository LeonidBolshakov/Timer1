########################################################
#                                                      #
# Timer with stages                                    #
#                                                      #
# Name structure                                       #
#                                                      #
# [1]_[2]_[3]_[4]                                      #
# where                                                #
# [1] - type/unit                                      #
# [2] - Time / number of stages                        #
# [3] - essence                                        #
# [4] - clarification                                  #
#                                                      #
########################################################

from sys import exit as sys_exit

import customtkinter as ctki
import tkinter as tk
import constant as c


#
# Customtkinter tools to ensure the timer works
#

class TimerTK:

    # Class object initialization parameters:
    #   root            - root object - window
    #   timer_operation - a function that performs the actual actions of the timer
    #

    def __init__(self, root, timer_operation):

        self._root_ = root
        self._timer_operation_ = timer_operation

        self.entry_time_stage_m = tk.StringVar()
        self.entry_time_stage_s = tk.StringVar()
        self.entry_number_of_stage = tk.StringVar()

        self.label_time_stage_left = ctki.CTkLabel(self._root_)
        self.label_time_total_left = ctki.CTkLabel(self._root_)

        self.signal_end_of_programm = False
        self.list_melodies = []
        self.ending_melody = ''
        self.button_start = ctki.CTkButton(self._root_)

        self._check_time_ = (self._root_.register(self._check_m_s_), '%P')
        self._check_stage_ = (self._root_.register(self._check_number_of_stage_), '%P')

        self._root_.geometry('200x300')
        self._root_.resizable(False, False)
        self._root_.title('Таймер')

    #
    #   Selecting a melody for the end of the timer
    def melody_comback(self, selected_melody):
        self.ending_melody = selected_melody

    #
    #   Handling the user's request to exit the program
    def stop(self):

        with open(c.SETTING_FILE, 'w') as file_setting:
            file_setting.write(self.entry_time_stage_m.get() + '\n')
            file_setting.write(self.entry_time_stage_s.get() + '\n')
            file_setting.write(self.entry_number_of_stage.get() + '\n')
            file_setting.write(self.ending_melody + '\n')

        self.signal_end_of_programm = True
        self._root_.protocol('WM_DELETE_WINDOW', sys_exit())

    #
    #   Checking the input of minutes/seconds characters
    def _check_m_s_(self, newvalue):
        newvalue = newvalue if newvalue != '' else '0'
        if newvalue.isnumeric():
            if 0 <= int(newvalue) < 60:
                return True
        self._root_.bell()
        return False

    #
    #   control of entering characters of the number of stages
    def _check_number_of_stage_(self, newvalue):
        newvalue = newvalue if newvalue != '' else '0'
        if newvalue.isnumeric():
            return True
        self._root_.bell()
        return False

    def _create_label_(self, text, x, y):
        lbl = ctki.CTkLabel(self._root_, text=text)
        lbl.place(x=x, y=y)

        return lbl

    def _create_entry_(self, x, y, tv, check):
        entry = ctki.CTkEntry(self._root_, validate='all', validatecommand=check,
                              textvariable=tv, justify='right', width=30)
        entry.place(x=x, y=y)

    def _create_button_(self, text, x, y, command):
        button = ctki.CTkButton(self._root_, text=text, width=70, command=command)
        button.place(x=x, y=y)

        return button

    def _create_combobox_(self, x, y, values, start_value, command=None):
        combobox = ctki.CTkComboBox(self._root_, values=values, command=command)
        combobox.set(start_value)
        combobox.place(x=x, y=y)

    def create_widgets(self):
        self._create_label_('Время этапа', x=22, y=0)
        self._create_label_('Мин', x=22, y=20)
        self._create_label_(':', x=50, y=20)
        self._create_label_(':', x=50, y=42)
        self._create_label_('Сек', x=55, y=20)
        self._create_label_('Осталось', x=120, y=20)
        self._create_label_('Количество этапов', x=22, y=75)
        self._create_label_(
            'Выбери мелодию завершения', x=10, y=170)
        self.label_time_stage_left = \
            self._create_label_('00:00', x=120, y=42)
        self.label_time_total_left = \
            self._create_label_('59:59', x=120, y=100)

        self._create_entry_(tv=self.entry_time_stage_m,
                            x=20, y=42, check=self._check_time_)
        self._create_entry_(tv=self.entry_time_stage_s,
                            x=53, y=42, check=self._check_time_)
        self._create_entry_(tv=self.entry_number_of_stage,
                            x=53, y=100, check=self._check_stage_)

        self.button_start = self._create_button_ \
            ('Пуск!', x=10, y=140, command=self._timer_operation_)
        self._create_button_('Выйти', x=120, y=140, command=self.stop)
        self._create_combobox_(x=10, y=190, values=self.list_melodies, start_value=self.ending_melody,
                               command=self.melody_comback)

    #
    #   calculate the number of seconds from the field information into minutes and seconds
    def create_sec_time_stage(self):

        str_time_m = self.entry_time_stage_m.get() if self.entry_time_stage_m.get() != '' else '0'
        str_time_s = self.entry_time_stage_s.get() if self.entry_time_stage_s.get() != '' else '0'

        return int(str_time_m) * 60 + int(str_time_s)

    #   Convert seconds to text "minutes:seconds"
    #
    @staticmethod
    def sec_to_str(sec):

        return f'{sec // 60 :02.0f}:{sec % 60 :02.0f}'

    def create_int_number_of_stage(self):

        str_number_of_stage = self.entry_number_of_stage.get() \
            if self.entry_number_of_stage.get() != '' else '1'
        return int(str_number_of_stage)
