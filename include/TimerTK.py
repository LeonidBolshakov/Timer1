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

import sys

import customtkinter as CTKi
import time

class TimerTK:
    def __init__(self, root, timer_operations):
        root.geometry( '200x300' )
        root.title( 'Таймер' )

        self._check_time_  = (root.register( self._check_m_s_ ), '%P')
        self._check_stage_ = (root.register( self._check_number_of_stage_ )), '%P'

        self.entry_time_stage_m = CTKi.CTkEntry( root )
        self.entry_time_stage_s = CTKi.CTkEntry( root )
        self.entry_number_of_stage = CTKi.CTkEntry( root )

        self.label_time_stage_left = CTKi.CTkLabel( root )
        self.label_time_total_left = CTKi.CTkLabel( root )

        self.button_start = CTKi.CTkButton( root )
        self.signal_end_of_programm = False

    def stop(self):
        self.signal_end_of_programm = True
        root.protocol( 'WM_DELETE_WINDOW', sys.exit())

    def _check_m_s_(self, newvalue):
        newvalue = newvalue if newvalue != '' else '0'
        if newvalue.isnumeric():
            if 0 <= int(newvalue) and int(newvalue) < 60:
                return True
        root.bell()
        return False

    def _check_number_of_stage_(self, newvalue):
        newvalue = newvalue if newvalue != '' else '0'
        if newvalue.isnumeric():
                return True
        root.bell()
        return False

    def _create_label_(self, text, x, y):
        lbl = CTKi.CTkLabel(root, text=text)
        lbl.place(x=x, y=y)
    
        return lbl
    
    def _create_entry_(self, x, y, check):
        entry = CTKi.CTkEntry( root, validate='key',
                               validatecommand=check, justify='right', width=30 )
        entry.place(x=x, y=y)
    
        return entry

    def _create_button_(self, text, x, y, command):
        button = CTKi.CTkButton(root, text=text, width=70, command=command)
        button.place(x=x, y=y)
    
        return button

    def create_widgets(self):
        self._create_label_( 'Мин',                 x= 22, y=  2 )
        self._create_label_( ':',                   x= 50, y=  2 )
        self._create_label_( ':',                   x= 50, y= 25 )
        self._create_label_( 'Сек',                 x= 55, y=  2 )
        self._create_label_( 'Осталось',            x=120, y=  2 )
        self._create_label_( 'Количество этапов',   x= 40, y= 60 )
        self.label_time_stage_left = \
            self._create_label_( '00:00',           x=120, y= 25 )
        self.label_time_total_left = \
            self._create_label_( '59:59',           x=120, y=100 )
        
        self.entry_time_stage_m    = \
            self._create_entry_(                    x= 20, y= 25, check=self._check_time_ )
        self.entry_time_stage_s    = \
            self._create_entry_(                    x= 53, y= 25, check=self._check_time_ )
        self.entry_number_of_stage = \
            self._create_entry_(                    x= 52, y=100, check=self._check_stage_ )

        self.button_start = self._create_button_\
            ( 'Пуск!',                              x=120, y=140, command=timer_operation )
        self.button_stop = self._create_button_\
            ( 'Выйти',                              x= 10, y=140, command=self.stop )

    def create_sec_time_stage(self):

        str_time_m = self.entry_time_stage_m.get() if self.entry_time_stage_m.get() != '' else '0'
        str_time_s = self.entry_time_stage_s.get() if self.entry_time_stage_s.get() != '' else '0'

        return int(str_time_m) * 60 + int(str_time_s)

    def sec_to_str(self, sec):

        return f'{sec // 60 :02.0f}:{sec % 60 :02.0f}'

    def create_int_number_of_stage(self):

        str_number_of_stage =   timer_tk.entry_number_of_stage.get() \
                                if timer_tk.entry_number_of_stage.get() != '' else '1'
        return int(str_number_of_stage)
