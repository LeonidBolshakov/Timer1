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
import time
from os import path, remove, walk
from sys import exit as sys_exit
from threading import Thread

import customtkinter as ctki
from playsound import playsound
from gtts import gTTS
from num2words import num2words

from TimTK import TimerTK
import constant as c


class MySleep:
    def __init__(self, sec):
        self.__zero_time = time.time()
        self.__sec = sec
        self.__seconds_passed = sec

    def end_of_cycle(self):
        if self.__zero_time + self.__seconds_passed <= time.time():
            self.__seconds_passed += self.__sec
            return True
        return False


root = ctki.CTk()


def create_list_melodies():
    result = []
    for root_, dirs, files in walk(c.MELODIES):
        for file in files:
            if path.splitext(file)[1] == '.mp3' or path.splitext(file)[1] == '.wav':
                result.append(file)

    return result


#
#   convert numbers to text and change masculine to feminine
#   Параметры:
#   tm      - number of minutes or seconds
#   min_sec - unit of measure tm (minutes or seconds)


def time_to_speach(tm, min_sec):
    unit_of_measure = {0: (' минут',  ' секунд'),
                       1: (' минута', ' секунда'),
                       2: (' минуты', ' секунды')}

    text = num2words(tm, lang='ru').replace('один', 'одна').replace('два', 'две') \
        .replace('дведцать', 'двадцать')
    if tm % 10 == 1 and tm != 11:
        text += unit_of_measure[1][min_sec]
    elif 1 < tm % 10 < 5 and not (11 < tm < 15):
        text += unit_of_measure[2][min_sec]
    else:
        text += unit_of_measure[0][min_sec]

    return text


#
#   we form the text and give it for sounding
def speach(sec_time_total_left):
    text_min = sec_time_total_left // 60
    text_sec = sec_time_total_left % 60

    if text_min == 0 and text_sec == 0:
        return
    if text_min == 0:
        text_of_speach = time_to_speach(text_sec, c.SECUNDES)
    elif text_sec == 0:
        text_of_speach = time_to_speach(text_min, c.MINUTES)
    else:
        text_of_speach = time_to_speach(text_min, c.MINUTES) + ',' + time_to_speach(text_sec, c.SECUNDES)
    s = gTTS(text_of_speach, lang='ru')
    if path.isfile(c.SPEECH_FILE):
        remove(c.SPEECH_FILE)
    s.save(c.SPEECH_FILE)
    Thread(target=playsound, args=(c.SPEECH_FILE,), daemon=True).start()


#
#   The actual operation of the timer
def timer_operation():
    timer_tk.button_start.configure(state=ctki.DISABLED, fg_color=c.DISABLE_COLOR)
    int_number_of_stage = timer_tk.create_int_number_of_stage()
    sec_time_total = timer_tk.create_sec_time_stage() * int_number_of_stage
    sec_time_stage = timer_tk.create_sec_time_stage()

    timer_tk.label_time_stage_left.configure(text=timer_tk.sec_to_str(sec_time_stage),
                                             text_color='SpringGreen3', font=('Arial Black', 18))
    timer_tk.label_time_total_left.configure(text=timer_tk.sec_to_str(sec_time_total),
                                             text_color='SpringGreen3', font=('Arial Black', 18))
    root.update()
    sec_time_total_left = sec_time_total
    my_sleep = MySleep(sec=1)
    for _ in range(int_number_of_stage):
        sec_time_stage_left = sec_time_stage
        for _ in range(sec_time_stage):
            if timer_tk.signal_end_of_programm:
                sys_exit()
            while not my_sleep.end_of_cycle():
                time.sleep(0.001)
            sec_time_total_left -= 1
            sec_time_stage_left -= 1
            timer_tk.label_time_total_left.configure(
                text=timer_tk.sec_to_str(sec_time_total_left))
            timer_tk.label_time_stage_left.configure(
                text=timer_tk.sec_to_str(sec_time_stage_left))
            root.update()

        speach(sec_time_total_left)

    melody_file = c.MELODIES + '/' + timer_tk.ending_melody
    if path.isfile(melody_file):
        Thread(target=playsound, args=(melody_file,)).start()
    timer_tk.stop()


#
#   Getting Started and Filling in Initial Values
timer_tk = TimerTK(root, timer_operation)

try:
    with open(c.SETTING_FILE, 'r') as file_setting:
        time_stage_m = file_setting.readline().strip()
        time_stage_s = file_setting.readline().strip()
        number_of_stage = file_setting.readline().strip()
        timer_tk.ending_melody = file_setting.readline().strip()

except FileNotFoundError:
    time_stage_m = '00'
    time_stage_s = '03'
    number_of_stage = '1'
    timer_tk.ending_melody = ''

timer_tk.list_melodies = create_list_melodies()
root.protocol('WM_DELETE_WINDOW', timer_tk.stop)
timer_tk.create_widgets()

timer_tk.entry_time_stage_m.set(time_stage_m)
timer_tk.entry_time_stage_s.set(time_stage_s)
timer_tk.entry_number_of_stage.set(number_of_stage)

root.mainloop()
