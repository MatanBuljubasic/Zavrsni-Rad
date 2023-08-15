from tkinter import *
from tkinter import ttk
from training_page import TrainingPage
import winsound
import time
import random
from constants import STIMULI
from pygame.mixer import music

class FrequencyBeginnerPage(TrainingPage):
    def __init__(self, parent, container):
        super().__init__(parent, container)

        self.info_label.config(text="You will hear two tones. Your task is to correctly\ndetect the latter tone as higher or lower.", font=('Times', 40))
        self.level = 1
        self.stimuli = STIMULI[0]
        self.more_info = "This exercise uses an analytic approach to auditory training. It trains your ability to differentiate similar frequencies."


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

        higher_button = ttk.Button(self.training_frame, text='Higher', style='my.TButton', command= lambda: [self.answer("higher", self.correct_a)])
        higher_button.grid(column=0, row=0)

        lower_button = ttk.Button(self.training_frame, text='Lower', style='my.TButton', command= lambda: [self.answer('lower', self.correct_a)])
        lower_button.grid(column=1, row=0)

        self.update()

        self.next_task()


    def next_task(self):
        self.stats_label.config(text=f'Task: {self.task_number+1}/10\nAccuracy: {self.accuracy:.3f}%')
        first_frequency = random.randint(150+self.modifier,16000-self.modifier)
        second_frequency = random.randint(first_frequency-self.modifier, first_frequency+self.modifier)
        music.load('Audio\\numbers\\1.wav')
        music.play()
        time.sleep(1)
        winsound.Beep(first_frequency, 1000)
        time.sleep(1)
        music.load('Audio\\numbers\\2.wav')
        music.play()
        time.sleep(1)
        winsound.Beep(second_frequency, 1000)
        if second_frequency > first_frequency:
            self.correct_a = "higher"
        else:
            self.correct_a = "lower"


            

            

class FrequencyIntermediatePage(TrainingPage):
    def __init__(self, parent, container):
        super().__init__(parent, container)

        self.info_label.config(text="You will hear three tones. Your task is to choose which\ntone is different from the other two.", font=('Times', 40))
        self.level = 2
        self.stimuli = STIMULI[0]
        self.more_info = "This exercise uses an analytic approach to auditory training. It trains your ability to differentiate similar frequencies and your ability to memorize previous sounds."


    def start_training(self):
        self.accuracy = 0
        self.task_number = 0
        self.stats_label = ttk.Label(self.stats_frame, text='')
        self.stats_label.grid(column=0, row=0)
        self.stats_label.config(font=('Times', 25))
        self.begin_button.grid_remove()
        self.correct = 0
        self.modifier = 3800
        self.correct_a = 0
        

        self.training_frame.columnconfigure(0, weight=1)
        self.training_frame.columnconfigure(1, weight=1)
        self.training_frame.columnconfigure(2, weight=1)

        first_button = ttk.Button(self.training_frame, text='Tone 1', style='my.TButton', command= lambda: [self.answer(1, self.correct_a)])
        first_button.grid(column=0, row=0)

        second_button = ttk.Button(self.training_frame, text='Tone 2', style='my.TButton', command= lambda: [self.answer(2, self.correct_a)])
        second_button.grid(column=1, row=0)

        third_button = ttk.Button(self.training_frame, text='Tone 3', style='my.TButton', command= lambda: [self.answer(3, self.correct_a)])
        third_button.grid(column=2, row=0)

        self.update()

        self.next_task()


    def next_task(self):
        self.stats_label.config(text=f'Task: {self.task_number+1}/10\nAccuracy: {float(self.accuracy):.3f}%')
        first_frequency = random.randint(150+self.modifier,16000-self.modifier)
        second_frequency = random.randint(first_frequency-self.modifier, first_frequency+self.modifier)
        self.correct_a = random.randint(1,3)
        for i in range(1,4):
            music.load(f'Audio\\numbers\\{i}.wav')
            music.play()
            time.sleep(1)
            if i == self.correct_a:
                winsound.Beep(first_frequency, 1000)
            else:
                winsound.Beep(second_frequency, 1000)

class FrequencyExpertPage(TrainingPage):
    def __init__(self, parent, container):
        super().__init__(parent, container)

        self.info_label.config(text="You will hear a tone. After that, you will hear two more\ndifferent tones. Your task is to decide which of the latter\ntones is closer to the first one.", font=('Times', 40))
        self.level = 3
        self.stimuli = STIMULI[0]
        self.more_info = "This exercise uses an analytic approach to auditory training. It trains your ability to differentiate similar frequencies and memorize previous sounds."


    def start_training(self):
        self.accuracy = 0
        self.task_number = 0
        self.stats_label = ttk.Label(self.stats_frame, text='')
        self.stats_label.grid(column=0, row=0)
        self.stats_label.config(font=('Times', 25))
        self.begin_button.grid_remove()
        self.correct = 0
        self.modifier = 3800
        self.correct_a = 0
        

        self.training_frame.columnconfigure(0, weight=1)
        self.training_frame.columnconfigure(1, weight=1)

        first_button = ttk.Button(self.training_frame, text='Tone 2', style='my.TButton', command= lambda: [self.answer(2, self.correct_a)])
        first_button.grid(column=0, row=0)

        second_button = ttk.Button(self.training_frame, text='Tone 3', style='my.TButton', command= lambda: [self.answer(3, self.correct_a)])
        second_button.grid(column=1, row=0)

        self.update()

        self.next_task()


    def next_task(self):
        self.stats_label.config(text=f'Task: {self.task_number+1}/10\nAccuracy: {float(self.accuracy):.3f}%')
        first_frequency = random.randint(150, 16000)
        second_frequency = random.randint(150+self.modifier,16000-self.modifier)
        third_frequency = random.randint(second_frequency-self.modifier, second_frequency+self.modifier)
        self.correct_a = random.randint(1,3)

        if abs(first_frequency - second_frequency) < abs(first_frequency - third_frequency):
            self.correct_a = 2
        else:
            self.correct_a = 3

        frequencies = [first_frequency, second_frequency, third_frequency]
        for i in range(1,4):
            music.load(f'Audio\\numbers\\{i}.wav')
            music.play()
            time.sleep(1)
            winsound.Beep(frequencies[i-1], 1000)