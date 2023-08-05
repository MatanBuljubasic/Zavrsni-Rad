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

        self.info_label = ttk.Label(self, text='', wraplength=self.winfo_screenwidth(), justify='center')
        self.info_label.grid(column=0, row=0)

        self.parent = parent

        self.training_frame = ttk.Frame(self, borderwidth=2, relief='solid')
        self.training_frame.grid(column=0, row=1, sticky='nsew')
        self.training_frame.grid_rowconfigure(0, weight=1)
        self.training_frame.grid_columnconfigure(0, weight=1)

        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.grid(column=0, row=2, sticky='nsew')
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(1, weight=1)

        self.settings_frame = ttk.Frame(self.bottom_frame)
        self.settings_frame.grid(column=0, row=0, sticky='nsew')
        self.settings_frame.columnconfigure(0, weight=1)
        self.settings_frame.columnconfigure(1, weight=1)

        self.stats_frame = ttk.Frame(self.bottom_frame)
        self.stats_frame.grid(column=1, row=0, sticky='nsew')
        self.stats_frame.columnconfigure(0, weight=1)
        self.stats_frame.columnconfigure(1, weight=1)

        quit_button = ttk.Button(self.stats_frame, text='Quit', style='my.TButton', command= lambda: [music.unload(), self.destroy(), self.parent.show_frame(self.parent.HomePage)])
        quit_button.grid(column=1, row=0,)

        self.begin_button = ttk.Button(self.training_frame, text='Begin', style='my.TButton', command= lambda: self.start_training())
        self.begin_button.grid(column=0, row=0)

    def answer(self, chosen, correct):
        self.task_number += 1
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
            self.create_window("results")
            self.parent.show_frame(self.parent.HomePage)

    def give_feedback(self, feedback):
        if feedback == True:
            self.create_window('good_feedback')
        else:
            self.create_window('bad_feedback')
        self.accuracy = (self.correct / self.task_number) * 100
        self.parent.update()
        self.update()


    def create_window(self, action):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        window_width = 300
        window_height = 300
        x = (screen_width/2) - (window_width/2)
        y = (screen_height/2) - (window_height/2)
        newWindow = Toplevel(self.parent)
        newWindow.title("Feedback")
        newWindow.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
        newWindow.grid_rowconfigure(0, weight=1)
        newWindow.grid_columnconfigure(0, weight=1)
        label = ttk.Label(newWindow, text="", wraplength=window_width, justify="center")
        label.grid(column=0, row=0)
        label.config(font=('Times', 25))
        if action == 'good_feedback':
            label.config(text="Well done!", foreground='green')
        elif action == 'bad_feedback':
            label.config(text=f"Incorrect!\nThe correct answer was '{self.correct_a}'.", foreground='red')
        else:
            label.config(text=f"Your results:\nTasks: {self.task_number}\nAccuracy: {self.accuracy:.3f}%")
        ok_button = ttk.Button(newWindow, text="Ok", command= lambda: [newWindow.destroy(), self.next_task()])
        ok_button.grid(column=0, row=1)
        