from tkinter import *
from tkinter import ttk
from training_page import TrainingPage
import winsound
from constants import STIMULI, SENTENCES
import pygame.mixer as mixer
from pygame.mixer import music
import random

class SentenceBeginnerPage(TrainingPage):
    def __init__(self, parent, container):
        super().__init__(parent, container)

        self.info_label.config(text="You will hear a sentence. You have to select\nwhich sentence you have heard.", font=('Times', 40))
        gender_label = ttk.Label(self.settings_frame, text='Choose the gender of the voice speaking:', font=('Times', 20))
        gender_label.grid(column=0, row=0)
        self.gender = StringVar(None, 'm')
        male_button = ttk.Radiobutton(self.settings_frame, text='Male', variable=self.gender, value='m')
        female_button = ttk.Radiobutton(self.settings_frame, text='Female', variable=self.gender, value='f')
        male_button.grid(column=0, row=1)
        female_button.grid(column=0, row=2)
        repeat_button = ttk.Button(self.settings_frame, text='Repeat', style='my.TButton', command= lambda: [mixer.Channel(0).play(mixer.Sound(f'Audio\\sentences\\{self.correct_a.replace("?", "_q").rstrip(".")}-{self.gender.get()}.wav'))])
        repeat_button.grid(column=1, row=1)
        self.level = 1
        self.stimuli = STIMULI[3]
        self.more_info = "This exercise uses a synthetic approach to auditory training. It trains your ability to recognize sentences."


    def start_training(self):
        self.accuracy = 0
        self.task_number = 0
        self.stats_label = ttk.Label(self.stats_frame, text='')
        self.stats_label.grid(column=0, row=0)
        self.stats_label.config(font=('Times', 25))
        self.begin_button.grid_remove()
        self.correct = 0
        self.modifier = 0
        self.correct_a = ""

        

        self.training_frame.rowconfigure(0, weight=1)
        self.training_frame.rowconfigure(1, weight=1)
        self.training_frame.rowconfigure(2, weight=1)


        self.first_button = ttk.Button(self.training_frame, text='', style='my.TButton', width=50, command= lambda: [self.answer(self.first_button.cget('text'), self.correct_a)])
        self.first_button.grid(column=0, row=0)

        self.second_button = ttk.Button(self.training_frame, text='', style='my.TButton', width=50, command= lambda: [self.answer(self.second_button.cget('text'), self.correct_a)])
        self.second_button.grid(column=0, row=1)

        self.third_button = ttk.Button(self.training_frame, text='', style='my.TButton', width=50, command= lambda: [self.answer(self.third_button.cget('text'), self.correct_a)])
        self.third_button.grid(column=0, row=2)

        self.update()

        self.next_task()

    def next_task(self):
        self.stats_label.config(text=f'Task: {self.task_number+1}/10\nAccuracy: {float(self.accuracy):.3f}%')
        rand_syll = random.sample(range(len(SENTENCES)), 3)
        correct = random.sample(rand_syll, 1)[0]
        self.correct_a = SENTENCES[correct]
        self.first_button.config(text=f'{SENTENCES[rand_syll[0]]}')
        self.second_button.config(text=f'{SENTENCES[rand_syll[1]]}')
        self.third_button.config(text=f'{SENTENCES[rand_syll[2]]}')
        self.update()
        mixer.Channel(0).play(mixer.Sound(f'Audio\\sentences\\{self.correct_a.replace("?", "_q").rstrip(".")}-{self.gender.get()}.wav'))

class SentenceIntermediatePage(TrainingPage):
    def __init__(self, parent, container):
        super().__init__(parent, container)

        self.info_label.config(text="You will hear a sentence with adaptive levels\n of background noise. Your task will be to select\nwhich sentence you have heard.", font=('Times', 40))
        gender_label = ttk.Label(self.settings_frame, text='Choose the gender of the voice speaking:', font=('Times', 20))
        gender_label.grid(column=0, row=0)
        self.gender = StringVar(None, 'm')
        male_button = ttk.Radiobutton(self.settings_frame, text='Male', variable=self.gender, value='m')
        female_button = ttk.Radiobutton(self.settings_frame, text='Female', variable=self.gender, value='f')
        male_button.grid(column=0, row=1)
        female_button.grid(column=0, row=2)
        repeat_button = ttk.Button(self.settings_frame, text='Repeat', style='my.TButton', command= lambda: [mixer.Channel(0).play(mixer.Sound(f'Audio\\sentences\\{self.correct_a.replace("?", "_q").rstrip(".")}-{self.gender.get()}.wav'))])
        repeat_button.grid(column=1, row=1)
        self.level = 2
        self.stimuli = STIMULI[3]
        self.more_info = "This exercise uses a synthetic approach to auditory training. It trains your ability to recognize sentences with the presence of background noise. After every correct or wrong answer, the volume of the background noise will increase or decrease, respectively."

    def start_training(self):
        self.accuracy = 0
        self.task_number = 0
        self.stats_label = ttk.Label(self.stats_frame, text='')
        self.stats_label.grid(column=0, row=0)
        self.stats_label.config(font=('Times', 25))
        self.begin_button.grid_remove()
        self.correct = 0
        self.modifier = 0
        self.correct_a = ""

        

        self.training_frame.rowconfigure(0, weight=1)
        self.training_frame.rowconfigure(1, weight=1)
        self.training_frame.rowconfigure(2, weight=1)


        self.first_button = ttk.Button(self.training_frame, text='', style='my.TButton', width=50, command= lambda: [self.answer(self.first_button.cget('text'), self.correct_a)])
        self.first_button.grid(column=0, row=0)

        self.second_button = ttk.Button(self.training_frame, text='', style='my.TButton', width=50, command= lambda: [self.answer(self.second_button.cget('text'), self.correct_a)])
        self.second_button.grid(column=0, row=1)

        self.third_button = ttk.Button(self.training_frame, text='', style='my.TButton', width=50, command= lambda: [self.answer(self.third_button.cget('text'), self.correct_a)])
        self.third_button.grid(column=0, row=2)

        music.load('Audio\\background\\crowd.wav')
        music.set_volume(self.modifier)
        music.play()

        self.update()

        self.next_task()

    def next_task(self):
        self.stats_label.config(text=f'Task: {self.task_number+1}/10\nAccuracy: {float(self.accuracy):.3f}%')
        music.set_volume((self.modifier*-1)/3800)
        rand_syll = random.sample(range(len(SENTENCES)), 3)
        correct = random.sample(rand_syll, 1)[0]
        self.correct_a = SENTENCES[correct]
        self.first_button.config(text=f'{SENTENCES[rand_syll[0]]}')
        self.second_button.config(text=f'{SENTENCES[rand_syll[1]]}')
        self.third_button.config(text=f'{SENTENCES[rand_syll[2]]}')
        self.update()
        mixer.Channel(0).play(mixer.Sound(f'Audio\\sentences\\{self.correct_a.replace("?", "_q").rstrip(".")}-{self.gender.get()}.wav'))

class SentenceExpertPage(TrainingPage):
    def __init__(self, parent, container):
        super().__init__(parent, container)

        self.info_label.config(text="You will hear a sentence with adaptive levels of background noise. Your task will be to write the sentence you have heard. Be careful of capitalizaion and interpunction.", font=('Times', 40))
        gender_label = ttk.Label(self.settings_frame, text='Choose the gender of the voice speaking:', font=('Times', 20))
        gender_label.grid(column=0, row=0)
        self.gender = StringVar(None, 'm')
        male_button = ttk.Radiobutton(self.settings_frame, text='Male', variable=self.gender, value='m')
        female_button = ttk.Radiobutton(self.settings_frame, text='Female', variable=self.gender, value='f')
        male_button.grid(column=0, row=1)
        female_button.grid(column=0, row=2)
        repeat_button = ttk.Button(self.settings_frame, text='Repeat', style='my.TButton', command= lambda: [mixer.Channel(0).play(mixer.Sound(f'Audio\\sentences\\{self.correct_a.replace("?", "_q").rstrip(".")}-{self.gender.get()}.wav'))])
        repeat_button.grid(column=1, row=1)
        self.level = 3
        self.stimuli = STIMULI[3]
        self.more_info = "This exercise uses a synthetic approach to auditory training. It trains your ability to recognize sentences with the presence of background noise, but without any offered options. After every correct or wrong answer, the volume of the background noise will increase or decrease, respectively."

    def start_training(self):
        self.accuracy = 0
        self.task_number = 0
        self.stats_label = ttk.Label(self.stats_frame, text='')
        self.stats_label.grid(column=0, row=0)
        self.stats_label.config(font=('Times', 25))
        self.begin_button.grid_remove()
        self.correct = 0
        self.modifier = 0
        self.correct_a = ""

        

        self.training_frame.rowconfigure(0, weight=1)
        self.training_frame.rowconfigure(1, weight=1)


        answer = StringVar()
        self.answer_entry = ttk.Entry(self.training_frame, width=60, textvariable=answer, font=('Times', 22))
        self.answer_entry.grid(column=0, row=0)

        self.submit_button = ttk.Button(self.training_frame, text='Submit', style='my.TButton', command= lambda: [self.answer(answer.get(), self.correct_a), self.answer_entry.delete(0, END)])
        self.submit_button.grid(column=0, row=1)

        music.load('Audio\\background\\crowd.wav')
        music.set_volume(self.modifier)
        music.play()

        self.update()

        self.next_task()

    def next_task(self):
        self.stats_label.config(text=f'Task: {self.task_number+1}/10\nAccuracy: {float(self.accuracy):.3f}%')
        music.set_volume((self.modifier*-1)/3800)
        rand_syll = random.sample(range(len(SENTENCES)), 3)
        correct = random.sample(rand_syll, 1)[0]
        self.correct_a = SENTENCES[correct]
        if '?' not in self.correct_a:
            self.correct_a = self.correct_a + '.'
        self.update()
        mixer.Channel(0).play(mixer.Sound(f'Audio\\sentences\\{self.correct_a.replace("?", "_q").rstrip(".")}-{self.gender.get()}.wav'))