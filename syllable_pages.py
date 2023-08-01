from tkinter import *
from tkinter import ttk
from training_page import TrainingPage
import winsound
import time
import random
from constants import STIMULI, SYLLABLES, SYLLABLES_WORDS, WORDS_S, SIMILAR_SYLLABLES
import pygame.mixer as mixer
from pygame.mixer import music

class SyllableBeginnerPage(TrainingPage):
    def __init__(self, parent, container):
        super().__init__(parent, container)

        self.info_label.config(text="You will hear a syllable with adaptive levels of background noise. Your task is to choose \nwhich syllable you have heard.", font=('Times', 40))
        gender_label = ttk.Label(self.settings_frame, text='Choose the gender of the voice speaking:', font=('Times', 20))
        gender_label.grid(column=0, row=0)
        self.gender = StringVar(None, 'm')
        male_button = ttk.Radiobutton(self.settings_frame, text='Male', variable=self.gender, value='m')
        female_button = ttk.Radiobutton(self.settings_frame, text='Female', variable=self.gender, value='f')
        male_button.grid(column=0, row=1)
        female_button.grid(column=0, row=2)
        self.level = 1
        self.stimuli = STIMULI[1]


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

        

        self.training_frame.columnconfigure(0, weight=1)
        self.training_frame.columnconfigure(1, weight=1)
        self.training_frame.columnconfigure(2, weight=1)


        self.first_button = ttk.Button(self.training_frame, text='', style='my.TButton', command= lambda: [self.answer(self.first_button.cget('text'), self.correct_a)])
        self.first_button.grid(column=0, row=0)

        self.second_button = ttk.Button(self.training_frame, text='', style='my.TButton', command= lambda: [self.answer(self.second_button.cget('text'), self.correct_a)])
        self.second_button.grid(column=1, row=0)

        self.third_button = ttk.Button(self.training_frame, text='', style='my.TButton', command= lambda: [self.answer(self.third_button.cget('text'), self.correct_a)])
        self.third_button.grid(column=2, row=0)

        music.load('Audio\\background\\crowd.wav')
        music.set_volume(self.modifier)
        music.play()

        self.update()

        self.next_task()

    def next_task(self):
        self.stats_label.config(text=f'Task: {self.task_number+1}/10\nAccuracy: {float(self.accuracy):.3f}%')
        music.set_volume((self.modifier*-1)/3800)
        rand_syll = random.sample(range(len(SYLLABLES)), 3)
        correct = random.sample(rand_syll, 1)[0]
        self.correct_a = SYLLABLES[correct]
        self.first_button.config(text=f'{SYLLABLES[rand_syll[0]]}')
        self.second_button.config(text=f'{SYLLABLES[rand_syll[1]]}')
        self.third_button.config(text=f'{SYLLABLES[rand_syll[2]]}')
        self.update()
        mixer.Channel(0).play(mixer.Sound(f'Audio\\syllables\\{self.correct_a.lower()}-{self.gender.get()}.wav'))

class SyllableIntermediatePage(TrainingPage):
    def __init__(self, parent, container):
        super().__init__(parent, container)

        self.info_label.config(text="You will hear a syllable with adaptive levels of background noise. Your task is to choose \nwhich word is the syllable from.", font=('Times', 40))
        gender_label = ttk.Label(self.settings_frame, text='Choose the gender of the voice speaking:', font=('Times', 20))
        gender_label.grid(column=0, row=0)
        self.gender = StringVar(None, 'm')
        male_button = ttk.Radiobutton(self.settings_frame, text='Male', variable=self.gender, value='m')
        female_button = ttk.Radiobutton(self.settings_frame, text='Female', variable=self.gender, value='f')
        male_button.grid(column=0, row=1)
        female_button.grid(column=0, row=2)
        self.level = 2
        self.stimuli = STIMULI[1]


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
        

        self.training_frame.columnconfigure(0, weight=1)
        self.training_frame.columnconfigure(1, weight=1)
        self.training_frame.columnconfigure(2, weight=1)


        self.first_button = ttk.Button(self.training_frame, text='', style='my.TButton', command= lambda: [self.answer(self.first_button.cget('text'), self.correct_a)])
        self.first_button.grid(column=0, row=0)

        self.second_button = ttk.Button(self.training_frame, text='', style='my.TButton', command= lambda: [self.answer(self.second_button.cget('text'), self.correct_a)])
        self.second_button.grid(column=1, row=0)

        self.third_button = ttk.Button(self.training_frame, text='', style='my.TButton', command= lambda: [self.answer(self.third_button.cget('text'), self.correct_a)])
        self.third_button.grid(column=2, row=0)

        music.load('Audio\\background\\crowd.wav')
        music.set_volume(self.modifier)
        music.play()

        self.update()

        self.next_task()

    def next_task(self):
        self.stats_label.config(text=f'Task: {self.task_number+1}/10\nAccuracy: {float(self.accuracy):.3f}%')
        rand_word = random.sample(range(1, len(WORDS_S)), 3)
        rand_syll = random.randint(0,1)
        correct = random.sample(rand_word, 1)[0]
        self.correct_a = WORDS_S[correct]
        self.first_button.config(text=f'{WORDS_S[rand_word[0]]}')
        self.second_button.config(text=f'{WORDS_S[rand_word[1]]}')
        self.third_button.config(text=f'{WORDS_S[rand_word[2]]}')
        self.update()
        mixer.Channel(0).play(mixer.Sound(f'Audio\\syllables\\{SYLLABLES_WORDS[self.correct_a][rand_syll]}-{self.gender.get()}.wav'))


class SyllableExpertPage(TrainingPage):
    def __init__(self, parent, container):
        super().__init__(parent, container)

        self.info_label.config(text="You will hear a syllable with adaptive levels of background noise. You will have to choose \nwhich syllable you have heard, but the options are similar.", font=('Times', 40))
        gender_label = ttk.Label(self.settings_frame, text='Choose the gender of the voice speaking:', font=('Times', 20))
        gender_label.grid(column=0, row=0)
        self.gender = StringVar(None, 'm')
        male_button = ttk.Radiobutton(self.settings_frame, text='Male', variable=self.gender, value='m')
        female_button = ttk.Radiobutton(self.settings_frame, text='Female', variable=self.gender, value='f')
        male_button.grid(column=0, row=1)
        female_button.grid(column=0, row=2)
        self.level = 3
        self.stimuli = STIMULI[1]


    def start_training(self):
        self.accuracy = 0
        self.task_number = 0
        self.stats_label = ttk.Label(self.stats_frame, text='')
        self.stats_label.grid(column=0, row=0)
        self.stats_label.config(font=('Times', 25))
        self.begin_button.grid_remove()
        self.correct = 0
        self.modifier = 3800
        self.correct_a = ""
        

        self.training_frame.columnconfigure(0, weight=1)
        self.training_frame.columnconfigure(1, weight=1)


        self.first_button = ttk.Button(self.training_frame, text='', style='my.TButton', command= lambda: [self.answer(self.first_button.cget('text'), str.capitalize(self.correct_a))])
        self.first_button.grid(column=0, row=0)

        self.second_button = ttk.Button(self.training_frame, text='', style='my.TButton', command= lambda: [self.answer(self.second_button.cget('text'), str.capitalize(self.correct_a))])
        self.second_button.grid(column=1, row=0)

        music.load('Audio\\background\\crowd.wav')
        music.set_volume(self.modifier)
        music.play()

        self.update()

        self.next_task()

    def next_task(self):
        self.stats_label.config(text=f'Task: {self.task_number+1}/10\nAccuracy: {float(self.accuracy):.3f}%')
        rand_pair = random.sample(range(len(SIMILAR_SYLLABLES)), 1)[0]
        rand_syll = random.randint(0,1)
        self.correct_a = SIMILAR_SYLLABLES[rand_pair][rand_syll]
        self.first_button.config(text=f'{str.capitalize(SIMILAR_SYLLABLES[rand_pair][0])}')
        self.second_button.config(text=f'{str.capitalize(SIMILAR_SYLLABLES[rand_pair][1])}')
        self.update()
        mixer.Channel(0).play(mixer.Sound(f'Audio\\syllables\\{self.correct_a}-{self.gender.get()}.wav'))