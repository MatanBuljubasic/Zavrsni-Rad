from tkinter import *
from tkinter import ttk
import random
from datetime import datetime
from pygame.mixer import music

class TrainingPage(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 3)
        self.rowconfigure(2, weight = 1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.info_label = ttk.Label(self, text='', wraplength=self.winfo_screenwidth(), justify="center")
        #center and wrap
        self.info_label.grid(column=0, row=0)

        self.parent = parent

        self.training_frame = ttk.Frame(self)
        self.training_frame.grid(column=0, row=1, sticky='nsew')
        self.training_frame.grid_rowconfigure(0, weight=1)
        self.training_frame.grid_columnconfigure(0, weight=1)

        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.grid(column=0, row=2, sticky='nsew')
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(1, weight=1)

        self.settings_frame = ttk.Frame(self.bottom_frame)
        self.settings_frame.grid(column=0, row=0, sticky='nsew')

        self.stats_frame = ttk.Frame(self.bottom_frame)
        self.stats_frame.grid(column=1, row=0, sticky='nsew')

        self.begin_button = ttk.Button(self.training_frame, text='Begin', style='my.TButton', command= lambda: self.start_training())
        self.begin_button.grid(column=0, row=0)

    def answer(self, chosen, correct):
        self.task_number += 1
        # 10 vježbi!!!!!!!!!!
        if self.task_number < 10:
            if correct == chosen:
                self.correct += 1
                self.modifier -= 380
                if random.random() < 0.7:
                    self.give_feedback(True)
                else:
                    self.accuracy = (self.correct / self.task_number) * 100
                    self.next_task()
            else:
                self.modifier += 380
                self.give_feedback(False)
        else:
            if correct == chosen:
                self.correct += 1
            self.accuracy = (self.correct / self.task_number) * 100
            data = {
                "level": self.level,
                "stimuli": self.stimuli,
                "accuracy": self.accuracy,
                "date": str(datetime.now())
            }
            music.unload()
            self.parent.db.child('users').child(self.parent.user_id).child("results").push(data)
            self.destroy()
            self.parent.show_frame(self.parent.HomePage)

    def give_feedback(self, feedback):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        window_width = 200
        window_height = 200
        x = (screen_width/2) - (window_width/2)
        y = (screen_height/2) - (window_height/2)
        
        newWindow = Toplevel(self.parent)
        newWindow.title("New Window")
        newWindow.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
        newWindow.grid_rowconfigure(0, weight=1)
        newWindow.grid_columnconfigure(0, weight=1)
        if feedback == True:
            label = ttk.Label(newWindow, text="Well done!", wraplength=window_width, justify="center")
            label.grid(column=0, row=0)
            label.config(font=('Times', 25), foreground='green')
        else:
            label = ttk.Label(newWindow, text=f"Incorrect!\nThe correct answer was '{self.correct_a}'.", wraplength=window_width, justify="center")
            label.grid(column=0, row=0)
            label.config(font=('Times', 25), foreground='red')
        self.accuracy = (self.correct / self.task_number) * 100
        self.parent.update()
        self.update()
        ok_button = ttk.Button(newWindow, text="Ok", command= lambda: [newWindow.destroy(), self.next_task()])
        ok_button.grid(column=0, row=1)
        