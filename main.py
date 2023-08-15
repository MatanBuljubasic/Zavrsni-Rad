from tkinter import *
from tkinter import ttk
import pyrebase 
from firebase_admin import auth
import re
from frequency_pages import *
from training_page import *
from syllable_pages import *
from word_pages import *
from sentence_pages import *
from registration_pages import *
from stats_pages import *
from constants import STIMULI
import pygame
from datetime import datetime



class App(Tk):
    def __init__(self):
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()
        x = (screen_width/2) - (window_width/2)
        y = (screen_height/2) - (window_height/2)

        self.title("Auditory Training")
        self.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
        self.minsize(1280,720)
        self.resizable(True,True)
        self.state('zoomed')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.option_add("*Label.Font", "aerial 30 bold")
        # s=ttk.Style(self)
        # self.tk.call('lappend', 'auto_path', 'Theme\\awthemes-10.4.0')
        # self.tk.call('package', 'require', 'awclearlooks')
        # s.theme_use('awclearlooks')

        firebase_config = {"apiKey": "AIzaSyBzdiZrsDOQj0NjiqCETgDQ6v6zJ4TZXII",
            "authDomain": "auditory-training-database.firebaseapp.com",
            "databaseURL": "https://auditory-training-database-default-rtdb.europe-west1.firebasedatabase.app",
            "projectId": "auditory-training-database",
            "storageBucket": "auditory-training-database.appspot.com",
            "messagingSenderId": "807211390848",
            "appId": "1:807211390848:web:4b71ac984196f0ca051365",
            "measurementId": "G-1857S2T78F",
            "serviceAccount": "auditory-training-database-firebase-adminsdk-w0s4a-9f07f35f8a.json"
        }
        firebase = pyrebase.initialize_app(firebase_config)
        self.auth = firebase.auth()
        self.db = firebase.database()
        self.user_id = ""

        pygame.init()


        self.container = ttk.Frame(self)
        self.container.grid(column=0, row=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        b = ttk.Style()
        b.configure('my.TButton', font=('Times', 28))


        self.frames = {}
        self.LandingPage = LandingPage
        self.LoginPage = LoginPage
        self.RegisterPage = RegisterPage
        self.HomePage = HomePage
        self.StimuliPage = StimuliPage
        self.PreTrainingPage = PreTrainingPage



        for F in {LandingPage, LoginPage, RegisterPage, HomePage, StimuliPage, PreTrainingPage}:
            self.init_frame(F)
            
        self.show_frame(LandingPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.grid(row=0, column=0, sticky="nsew")

    def hide_frame(self, cont):
        frame = self.frames[cont]
        frame.grid_forget()

    def init_frame(self, F):
        frame = F(self, self.container)
        self.frames[F] = frame

class HomePage(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(1, weight = 2)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.email_label = ttk.Label(self, text='')
        self.email_label.grid(column=0, row=0)

        choose_label = ttk.Label(self, text="Check your statistics or begin training.")
        choose_label.grid(column=0, row=1)
        choose_label.config(font=('Times', 30))

        self.training_img = PhotoImage(file='Images\\training.png')
        training_button = ttk.Button(self, text='Begin training', style="my.TButton", command= lambda: [parent.hide_frame(HomePage), parent.show_frame(StimuliPage)], image=self.training_img, compound=LEFT)
        training_button.grid(column=0, row=2, sticky="nsew", padx=(500), pady=(20,20))

        self.stats_img = PhotoImage(file='Images\\stats.png')
        stats_button = ttk.Button(self, text='View statistics', style="my.TButton",  command= lambda: [parent.hide_frame(HomePage), parent.init_frame(StatsPage), parent.show_frame(StatsPage)], image=self.stats_img, compound=LEFT)
        stats_button.grid(column=0, row=3, sticky="nsew", padx=(500), pady=(20,20))

        logout_button = ttk.Button(self, text='Sign out', style="my.TButton", command= lambda: [self.logout_user(), parent.hide_frame(StimuliPage), parent.show_frame(LandingPage)])
        logout_button.grid(column=0, row=4, sticky='sw')

    def logout_user(self):
        auth.current_user = None

    def add_user(self, parent):
        email = parent.db.child("users").child(parent.user_id).child("email").get()
        self.email_label.config(text=f'Welcome, {email.val()}!', font=('Times', 40))

class StimuliPage(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        choose_label = ttk.Label(self, text="Please choose the type of auditory stimulus you want to train.")
        choose_label.grid(column=0, row=0)
        choose_label.config(font=('Times', 30))

        self.freq_img = PhotoImage(file='Images\\freq.png')
        frequencies_button = ttk.Button(self, text='Frequencies', style="my.TButton", command= lambda: [parent.hide_frame(StimuliPage), self.choose_stimuli(parent, STIMULI[0])], image=self.freq_img, compound=LEFT)
        frequencies_button.grid(column=0, row=1, sticky="nsew", padx=(500), pady=(20,20))

        self.syll_img = PhotoImage(file='Images\\syllables.png')
        syllables_button = ttk.Button(self, text='Syllables', style="my.TButton",  command= lambda: [parent.hide_frame(StimuliPage), self.choose_stimuli(parent, STIMULI[1])], image=self.syll_img, compound=LEFT)
        syllables_button.grid(column=0, row=2, sticky="nsew", padx=(500), pady=(20,20))

        self.word_img = PhotoImage(file='Images\\words.png')
        words_button = ttk.Button(self, text='Words', style="my.TButton",  command= lambda: [parent.hide_frame(StimuliPage), self.choose_stimuli(parent, STIMULI[2])], image=self.word_img, compound=LEFT)
        words_button.grid(column=0, row=3, sticky="nsew", padx=(500), pady=(20,20))

        self.sent_img = PhotoImage(file='Images\\sentences.png')
        sentences_button = ttk.Button(self, text='Sentences', style="my.TButton",  command= lambda: [parent.hide_frame(StimuliPage), self.choose_stimuli(parent, STIMULI[3])], image=self.sent_img, compound=LEFT)
        sentences_button.grid(column=0, row=4, sticky="nsew", padx=(500), pady=(20,20))

        back_button = ttk.Button(self, text='Back', style="my.TButton", command= lambda: [parent.hide_frame(StimuliPage), parent.show_frame(HomePage)])
        back_button.grid(column=0, row=5, sticky='sw')

    def choose_stimuli(self, parent, stimuli):
        page = parent.frames[PreTrainingPage]
        page.add_info(stimuli, parent)
        parent.show_frame(PreTrainingPage)

class PreTrainingPage(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(1, weight = 2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        self.level_frame = ttk.Frame(self)
        self.level_frame.grid(column=0, row=1, sticky='nsew')
        self.level_frame.columnconfigure(0, weight=1)
        self.level_frame.columnconfigure(1, weight=1)
        self.level_frame.columnconfigure(2, weight=1)
        self.level_frame.rowconfigure(0, weight=1)
        self.level_frame.rowconfigure(1, weight=1)
        self.level_frame.rowconfigure(2, weight=1)
        self.level_frame.rowconfigure(3, weight=1)
        self.level_frame.grid_columnconfigure(0, weight=1)
        self.level_frame.grid_rowconfigure(0, weight=1)

        self.instruction_label = ttk.Label(self, text='')
        self.instruction_label.grid(column=0, row=0)
        self.instruction_label.config(font=('Times', 40))

        self.beginner_info = ttk.Label(self.level_frame, text="", font=('Times', 18), width=self.winfo_screenwidth()/3, wraplength=self.winfo_screenwidth()/3)
        self.beginner_info.grid(column=0, row=0, sticky="w", padx=(20,20))

        self.beginner_button = ttk.Button(self.level_frame, text='Beginner', style="my.TButton", command= lambda: [parent.hide_frame(PreTrainingPage), parent.show_frame(FrequencyBeginnerPage)])
        self.beginner_button.grid(column=1, row=0, pady=(20,20), sticky='nsew')
        
        self.beginner_label = ttk.Label(self.level_frame, text="")
        self.beginner_label.grid(column=2, row=0, sticky="w", padx=(20,0))

        self.intermediate_info = ttk.Label(self.level_frame, text="", font=('Times', 18), width=self.winfo_screenwidth()/3, wraplength=self.winfo_screenwidth()/3)
        self.intermediate_info.grid(column=0, row=1, sticky="w", padx=(20,20))

        self.intermediate_button = ttk.Button(self.level_frame, text='Intermediate', style="my.TButton", command= lambda: [parent.hide_frame(PreTrainingPage), parent.show_frame(FrequencyIntermediatePage)])
        self.intermediate_button.grid(column=1, row=1, pady=(20,20), sticky='nsew')
        
        self.intermediate_label = ttk.Label(self.level_frame, text='')
        self.intermediate_label.grid(column=2, row=1, sticky="w", padx=(20,0))

        self.expert_info = ttk.Label(self.level_frame, text="", font=('Times', 18), width=self.winfo_screenwidth()/3, wraplength=self.winfo_screenwidth()/3)
        self.expert_info.grid(column=0, row=2, sticky="w", padx=(20,20))

        self.expert_button = ttk.Button(self.level_frame, text='Expert', style="my.TButton", command= lambda: [parent.hide_frame(PreTrainingPage), parent.show_frame(FrequencyExpertPage)])
        self.expert_button.grid(column=1, row=2, pady=(20,20), sticky='nsew')
        
        self.expert_label = ttk.Label(self.level_frame, text='')
        self.expert_label.grid(column=2, row=2, sticky="w", padx=(20,0))

        back_button = ttk.Button(self.level_frame, text='Back', style='my.TButton', command= lambda: [parent.hide_frame(PreTrainingPage), parent.show_frame(StimuliPage)])
        back_button.grid(column=0, row=3, sticky="sw")

        
    def add_info(self,stimuli, parent):
        self.doc = parent.db.child("users").child(parent.user_id).child("results").get()
        results = self.doc.val()
        self.instruction_label.config(text=f'Choose the difficulty level for {stimuli} training')
        self.stimuli = stimuli
        if results == None:
            beginner_stats = {
                "median":"Not available",
                "best":"Not available",
                "last":"Not available"
            }
            intermediate_stats = {
                "median":"Not available",
                "best":"Not available",
                "last":"Not available"
            }
            expert_stats = {
                "median":"Not available",
                "best":"Not available",
                "last":"Not available"
            }
        else:
            beginner_results = []
            intermediate_results = []
            expert_results = []
            stimuli_results = list(filter(self.filter_stimuli, results.values()))
            for result in stimuli_results:
                if result['level'] == 1:
                    beginner_results.append(result)
                elif result['level'] == 2:
                    intermediate_results.append(result)
                else:
                    expert_results.append(result)
            beginner_stats = self.calculate_stats(beginner_results)
            intermediate_stats = self.calculate_stats(intermediate_results)
            expert_stats = self.calculate_stats(expert_results)

        self.beginner_label.config(text=f"Last score: {beginner_stats['last']}%\nBest score: {beginner_stats['best']}%\nAverage score: {beginner_stats['median']}%", font=('Times', 18))
        self.intermediate_label.config(text=f"Last score: {intermediate_stats['last']}%\nBest score: {intermediate_stats['best']}%\nAverage score: {intermediate_stats['median']}%", font=('Times', 18))
        self.expert_label.config(text=f"Last score: {expert_stats['last']}%\nBest score: {expert_stats['best']}%\nAverage score: {expert_stats['median']}%", font=('Times', 18))
        #kako prikazati samo dvije decimale, ako postoji mogućnost da je string a ne broj?
        if stimuli == STIMULI[0]:
            self.beginner_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(FrequencyBeginnerPage), parent.show_frame(FrequencyBeginnerPage)])
            self.intermediate_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(FrequencyIntermediatePage), parent.show_frame(FrequencyIntermediatePage)])
            self.expert_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(FrequencyExpertPage), parent.show_frame(FrequencyExpertPage)])
            self.beginner_info.config(text='You will hear two tones. Your task is to correctly detect the latter tone as higher or lower.')
            self.intermediate_info.config(text='You will hear three tones. Your task is to choose which tone is different from the other two.')
            self.expert_info.config(text='You will hear a tone. After that, you will hear two more different tones. Your task is to decide which of the latter tones is closer to the first one.')
        elif stimuli == STIMULI[1]:
            self.beginner_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(SyllableBeginnerPage), parent.show_frame(SyllableBeginnerPage)])
            self.intermediate_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(SyllableIntermediatePage), parent.show_frame(SyllableIntermediatePage)])
            self.expert_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(SyllableExpertPage), parent.show_frame(SyllableExpertPage)])
            self.beginner_info.config(text='You will hear a syllable with adaptive levels of background noise. Your task is to choose which syllable you have heard.')
            self.intermediate_info.config(text='You will hear a syllable with adaptive levels of background noise. Your task is to choose which word is the syllable from.')
            self.expert_info.config(text='You will hear a syllable with adaptive levels of background noise. You will have to choose which syllable you have heard, but the options are similar.')
        elif stimuli == STIMULI[2]:
            self.beginner_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(WordBeginnerPage), parent.show_frame(WordBeginnerPage)])
            self.intermediate_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(WordIntermediatePage), parent.show_frame(WordIntermediatePage)])
            self.expert_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(WordExpertPage), parent.show_frame(WordExpertPage)])
            self.beginner_info.config(text='You will hear a word. Your task is to choose the word you have heard.')
            self.intermediate_info.config(text='You will hear a word with adaptive levels of background noise. Your task is to choose the word you have heard.')
            self.expert_info.config(text='You will hear a word with adaptive levels of background noise. You will have to choose which word you have heard, but the options are similar.')
        else:
            self.beginner_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(SentenceBeginnerPage), parent.show_frame(SentenceBeginnerPage)])
            self.intermediate_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(SentenceIntermediatePage), parent.show_frame(SentenceIntermediatePage)])
            self.expert_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(SentenceExpertPage), parent.show_frame(SentenceExpertPage)])
            self.beginner_info.config(text='You will hear a sentence. You have to select which sentence you have heard.')
            self.intermediate_info.config(text='You will hear a sentence with adaptive levels of background noise. Your task will be to select which sentence you have heard.')
            self.expert_info.config(text='You will hear a sentence with adaptive levels of background noise. Your task will be to write the sentence you have heard. Be careful of capitalizaion and interpunction.')


    def calculate_stats(self, results):
        stats={}

        if len(results) != 0:
            stats["best"] = max(results, key=lambda x:x["accuracy"])["accuracy"]
            stats["last"] = max(results, key=lambda x:x["date"])["accuracy"]
            stats["median"] = float(sum(d['accuracy'] for d in results)) / len(results)
        else:
            stats = {
                "median":"Not available",
                "best":"Not available",
                "last":"Not available"
            }


        return stats
    
    def filter_stimuli(self, result):
        result['date'] = datetime.strptime(result['date'], "%Y-%m-%d %H:%M:%S.%f")
        if result['stimuli'] == self.stimuli:
            return True
        else:
            return False

if __name__ == "__main__":
    app = App()
    app.mainloop()
