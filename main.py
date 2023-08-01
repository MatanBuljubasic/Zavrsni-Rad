from tkinter import *
from tkinter import ttk
import pyrebase
import re
from frequency_pages import *
from training_page import *
from syllable_pages import *
from word_pages import *
from sentence_pages import *
from constants import STIMULI
import pygame




class App(Tk):
    def __init__(self):
        super().__init__()

        self.title("Auditory Training")
        self.geometry("1280x720")
        self.minsize(1280,720)
        self.resizable(True,True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.option_add("*Label.Font", "aerial 30 bold")
        # s=ttk.Style()
        # s.theme_use('clam')
        # povecaj font svagdje

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
        self.PreTrainingPage = PreTrainingPage



        for F in {LandingPage, LoginPage, RegisterPage, HomePage, PreTrainingPage}:
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



class LandingPage(ttk.Frame):

    def __init__(self, parent, container):
        super().__init__(container)

        landing_style = ttk.Style()
        landing_style.configure('My.TLanding', background='blue')
        
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 3)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        
        s = ttk.Style()
        s.configure('My.TFrame', background='red')

        title_frame = ttk.Frame(self, borderwidth=2, relief='raised', padding='0.5i')
        title_frame.grid(column=0, row=0)
        title_frame.grid_rowconfigure(0, weight=1)
        title_frame.grid_columnconfigure(0, weight=1)

        title_label = ttk.Label(title_frame, text="Welcome to auditory training!")
        title_label.grid(row=0, column=0, sticky="nsew")
        title_label.config(font=('Times', 36))

        mainframe = ttk.Frame(self)
        mainframe.grid(column=0, row=1)
        mainframe.grid_rowconfigure(0, weight=1)
        mainframe.grid_columnconfigure(0, weight=1)

        login_label = ttk.Label(mainframe, text="If you already have an account, click here to login:")
        login_label.grid(column=0, row=1, sticky="nsew", pady=(20,5))
        login_label.config(font=('Times', 16))
        login_button = ttk.Button(mainframe, text="Login", command=lambda: [parent.hide_frame(LandingPage), parent.show_frame(LoginPage)])
        login_button.grid(column=0, row=2, sticky="nsew")

        register_label = ttk.Label(mainframe, text="If you're a first time user, click here to create an account:")
        register_label.grid(column=0, row=3, sticky="w", pady=(20,5))
        register_label.config(font=('Times', 16))
        register_button = ttk.Button(mainframe, text="Create an account", command=lambda: [parent.hide_frame(LandingPage), parent.show_frame(RegisterPage)])
        register_button.grid(column=0, row=4, sticky="nsew")



class LoginPage(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        back_button = ttk.Button(self, text='Back', command= lambda: [parent.hide_frame(LoginPage), self.email_entry.delete(0, END), self.password_entry.delete(0, END), parent.show_frame(LandingPage)])
        back_button.grid(column=0, row=2, sticky="sw")

        login_frame = ttk.Frame(self)
        login_frame.grid(column=1, row=1)
        login_frame.grid_rowconfigure(0, weight=1)
        login_frame.grid_columnconfigure(0, weight=1)

        email_label = ttk.Label(login_frame, text="Email:")
        email_label.grid(column=0, row=0, sticky="nsew", padx=(0, 10), pady=(0,10))

        email = StringVar()
        self.email_entry = ttk.Entry(login_frame, width=30, textvariable=email)
        self.email_entry.grid(column=1, row=0, sticky="w", pady=(0,10))

        password_label = ttk.Label(login_frame, text="Password:")
        password_label.grid(column=0, row=1, sticky="nsew", pady=(0,10))

        password = StringVar()
        self.password_entry = ttk.Entry(login_frame, width=30, textvariable=password, show="*")
        self.password_entry.grid(column=1, row=1, sticky="w", pady=(0,10))

        self.toggle_button = ttk.Button(login_frame, text='Show Password', width=15, command= lambda: self.toggle_password())
        self.toggle_button.grid(column=2, row=1, sticky="nw")

        login_button = ttk.Button(login_frame, text="Login", command= lambda: [self.login(email, password, parent)])
        login_button.grid(column=1, row=2, sticky="e")

        self.error_message = StringVar()
        error_message_label = ttk.Label(login_frame, font='TkSmallCaptionFont', foreground='red', textvariable=self.error_message)
        error_message_label.grid(column=1, row=3, sticky="w")

    def login(self, email, password, parent):
        self.error_message.set('')
        try:
            user = parent.auth.sign_in_with_email_and_password(email.get(), password.get())
            parent.user_id = user['localId']
            parent.hide_frame(LoginPage)
            self.email_entry.delete(0, END)
            self.password_entry.delete(0, END)
            home_page = parent.frames[HomePage]
            home_page.add_user(parent)
            parent.show_frame(HomePage)
        except:
            self.error_message.set('Username or password is incorrect.')

    def toggle_password(self):
        if self.password_entry.cget('show') == '':
            self.password_entry.config(show='*')
            self.toggle_button.config(text='Show Password')
        else:
            self.password_entry.config(show='')
            self.toggle_button.config(text='Hide Password')
        

class RegisterPage(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.email_state=False
        self.password_state=False

        check_password_wrapper = (self.register(self.check_password), '%P')
        check_email_wrapper = (self.register(self.check_email), '%P')

        back_button = ttk.Button(self, text='Back', command= lambda: [parent.hide_frame(RegisterPage), self.email_entry.delete(0, END), self.password_entry.delete(0, END), self.error_message.set(''), self.email_message.set(''), self.password_message.set(''), parent.show_frame(LandingPage)])
        back_button.grid(column=0, row=2, sticky="sw")

        register_frame = ttk.Frame(self)
        register_frame.grid(column=1, row=1)
        register_frame.grid_rowconfigure(0, weight=1)
        register_frame.grid_columnconfigure(0, weight=1)

        email_label = ttk.Label(register_frame, text="Email:")
        email_label.grid(column=0, row=0, sticky="nsew", padx=(0, 10), pady=(0,10))

        email = StringVar()
        email.trace('w', self.check_both)
        self.email_entry = ttk.Entry(register_frame, width=30, textvariable=email, validate='focusout', validatecommand=check_email_wrapper)
        self.email_entry.grid(column=1, row=0, sticky="w", pady=(0,10))

        self.email_message = StringVar()
        email_message = ttk.Label(register_frame, font='TkSmallCaptionFont', foreground='red', textvariable=self.email_message)
        email_message.grid(column=1, row=1, sticky="nw")

        password_label = ttk.Label(register_frame, text="Password:")
        password_label.grid(column=0, row=2, sticky="nsew", pady=(0,10))

        password = StringVar()
        password.trace('w', self.check_both)
        self.password_entry = ttk.Entry(register_frame, width=30, textvariable=password, show="*", validate='focusout', validatecommand=check_password_wrapper)
        self.password_entry.grid(column=1, row=2, sticky="w", pady=(0,10))
        
        self.password_message = StringVar()
        password_message_label = ttk.Label(register_frame, font='TkSmallCaptionFont', foreground='red', textvariable=self.password_message)
        password_message_label.grid(column=1, row=3, sticky="nw")

        self.toggle_button = ttk.Button(register_frame, text='Show Password', width=15, command= lambda: self.toggle_password())
        self.toggle_button.grid(column=2, row=2, sticky="nw")

        self.register_button = ttk.Button(register_frame, text="Register", command= lambda: [self.register_user(email, password, parent)])
        self.register_button.grid(column=1, row=4, sticky="e")
        self.register_button.state(['disabled'])

        self.error_message = StringVar()
        self.error_message_label = ttk.Label(register_frame, font='TkSmallCaptionFont', foreground='red', textvariable=self.error_message)
        self.error_message_label.grid(column=1, row=5, sticky="e")

    def register_user(self, email, password, parent):
        self.error_message.set('')
        try:
            user = parent.auth.create_user_with_email_and_password(email.get(),password.get())
            parent.db.child("users").child(user['localId']).set({"email":user['email']})
        except:
            self.error_message.set('Email already exists!')
            return
        parent.hide_frame(RegisterPage)
        self.email_entry.delete(0, END)
        self.password_entry.delete(0, END)
        parent.show_frame(LandingPage)

            

    def check_password(self, value):
        self.password_message.set('')
        valid = re.match('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', value) is not None
        if valid:
            self.password_state = True
        else:
            self.password_state = False
            self.password_message.set('Password must have:\n- At least one alphabetic character\n(uppercase or lowercase)\n- At least one digit\n- Minimum length of 8 characters\n- No spaces')
        return valid

    def check_email(self, value):
        self.email_message.set('')
        valid = re.match("[a-z0-9]+@[a-z]+\.[a-z]{2,3}", value) is not None
        if valid:
            self.email_state = True
        else:
            self.email_state = False
            self.email_message.set('Email address is not valid.\nExample of valid email address:\njohn.doe@gmail.com')
        return valid
        # radi tek kad dodam razmak na kraj

    def check_both(self, *args):
        x = self.email_state
        y = self.password_state
        if x and y:
            self.register_button.state(['!disabled'])
        else:
            self.register_button.state(['disabled'])

    def toggle_password(self):
        if self.password_entry.cget('show') == '':
            self.password_entry.config(show='*')
            self.toggle_button.config(text='Show Password')
        else:
            self.password_entry.config(show='')
            self.toggle_button.config(text='Hide Password')

class HomePage(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(1, weight = 2)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.email_label = ttk.Label(self, text='')
        self.email_label.grid(column=0, row=0)

        choose_label = ttk.Label(self, text="Please choose the type of auditory stimulus you want to train.")
        choose_label.grid(column=0, row=1)
        choose_label.config(font=('Times', 30))


        frequencies_button = ttk.Button(self, text='Frequencies', style="my.TButton", command= lambda: [parent.hide_frame(HomePage), self.choose_stimuli(parent, STIMULI[0])])
        frequencies_button.grid(column=0, row=2, sticky="nsew", padx=(300,300), pady=(20,20))

        syllables_button = ttk.Button(self, text='Syllables', style="my.TButton",  command= lambda: [parent.hide_frame(HomePage), self.choose_stimuli(parent, STIMULI[1])])
        syllables_button.grid(column=0, row=3, sticky="nsew", padx=(300,300), pady=(20,20))

        words_button = ttk.Button(self, text='Words', style="my.TButton",  command= lambda: [parent.hide_frame(HomePage), self.choose_stimuli(parent, STIMULI[2])])
        words_button.grid(column=0, row=4, sticky="nsew", padx=(300,300), pady=(20,20))

        sentences_button = ttk.Button(self, text='Sentences', style="my.TButton",  command= lambda: [parent.hide_frame(HomePage), self.choose_stimuli(parent, STIMULI[3])])
        sentences_button.grid(column=0, row=5, sticky="nsew", padx=(300,300), pady=(20,20))
    
    def add_user(self, parent):
        email = parent.db.child("users").child(parent.user_id).child("email").get()
        self.email_label.config(text=f'Welcome, {email.val()}!', font=('Times', 40))

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
        self.level_frame.rowconfigure(0, weight=1)
        self.level_frame.rowconfigure(1, weight=1)
        self.level_frame.rowconfigure(2, weight=1)
        self.level_frame.rowconfigure(3, weight=1)
        self.level_frame.grid_columnconfigure(0, weight=1)
        self.level_frame.grid_rowconfigure(0, weight=1)

        self.instruction_label = ttk.Label(self, text='')
        self.instruction_label.grid(column=0, row=0)
        self.instruction_label.config(font=('Times', 40))

        self.beginner_button = ttk.Button(self.level_frame, text='Beginner', style="my.TButton", command= lambda: [parent.hide_frame(PreTrainingPage), parent.show_frame(FrequencyBeginnerPage)])
        self.beginner_button.grid(column=0, row=0, sticky="nse", pady=(20,20))
        
        
        self.beginner_label = ttk.Label(self.level_frame, text="")
        self.beginner_label.grid(column=1, row=0, sticky="w")

        self.intermediate_button = ttk.Button(self.level_frame, text='Intermediate', style="my.TButton", command= lambda: [parent.hide_frame(PreTrainingPage), parent.show_frame(FrequencyIntermediatePage)])
        self.intermediate_button.grid(column=0, row=1, sticky="nse", pady=(20,20))
        
        
        self.intermediate_label = ttk.Label(self.level_frame, text='')
        self.intermediate_label.grid(column=1, row=1, sticky="w")

        self.expert_button = ttk.Button(self.level_frame, text='Expert', style="my.TButton", command= lambda: [parent.hide_frame(PreTrainingPage), parent.show_frame(FrequencyExpertPage)])
        self.expert_button.grid(column=0, row=2, sticky="nse", pady=(20,20))
        
        
        self.expert_label = ttk.Label(self.level_frame, text='')
        self.expert_label.grid(column=1, row=2, sticky="w")

        back_button = ttk.Button(self.level_frame, text='Back', command= lambda: [parent.hide_frame(PreTrainingPage), parent.show_frame(HomePage)])
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

        self.beginner_label.config(text=f"Last score: {beginner_stats['last']}%\nBest score: {beginner_stats['best']}%\nAverage score: {beginner_stats['median']}%")
        self.intermediate_label.config(text=f"Last score: {intermediate_stats['last']}%\nBest score: {intermediate_stats['best']}%\nAverage score: {intermediate_stats['median']}%")
        self.expert_label.config(text=f"Last score: {expert_stats['last']}%\nBest score: {expert_stats['best']}%\nAverage score: {expert_stats['median']}%")
        #kako prikazati samo dvije decimale, ako postoji mogućnost da je string a ne broj?
        if stimuli == STIMULI[0]:
            self.beginner_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(FrequencyBeginnerPage), parent.show_frame(FrequencyBeginnerPage)])
            self.intermediate_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(FrequencyIntermediatePage), parent.show_frame(FrequencyIntermediatePage)])
            self.expert_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(FrequencyExpertPage), parent.show_frame(FrequencyExpertPage)])
        elif stimuli == STIMULI[1]:
            self.beginner_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(SyllableBeginnerPage), parent.show_frame(SyllableBeginnerPage)])
            self.intermediate_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(SyllableIntermediatePage), parent.show_frame(SyllableIntermediatePage)])
            self.expert_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(SyllableExpertPage), parent.show_frame(SyllableExpertPage)])
        elif stimuli == STIMULI[2]:
            self.beginner_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(WordBeginnerPage), parent.show_frame(WordBeginnerPage)])
            self.intermediate_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(WordIntermediatePage), parent.show_frame(WordIntermediatePage)])
            self.expert_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.init_frame(WordExpertPage), parent.show_frame(WordExpertPage)])
        else:
            self.beginner_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.show_frame(SentenceBeginnerPage)])
            self.intermediate_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.show_frame(SentenceIntermediatePage)])
            self.expert_button.config(command= lambda: [parent.hide_frame(PreTrainingPage), parent.show_frame(SentenceExpertPage)])


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
