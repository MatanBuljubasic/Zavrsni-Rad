from tkinter import *
from tkinter import ttk
from training_page import TrainingPage
import winsound

class SentenceBeginnerPage(TrainingPage):
    def __init__(self, parent, container):
        super().__init__(parent, container)

        self.info_label.config(text="You will hear a sentence with adaptive levels of background noise. You have to select whether or not you have heard every word correctly.")

class SentenceIntermediatePage(TrainingPage):
    def __init__(self, parent, container):
        super().__init__(parent, container)

        self.info_label.config(text="You will hear a sentence with adaptive levels of background noise. Your task will be to select which sentence you have heard.")

class SentenceExpertPage(TrainingPage):
    def __init__(self, parent, container):
        super().__init__(parent, container)

        self.info_label.config(text="You will hear a sentence with adaptive levels of background noise. Your task will be to write the sentence you have heard.")