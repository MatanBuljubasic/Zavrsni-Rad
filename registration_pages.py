from tkinter import *
from tkinter import ttk
import re


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
        login_button = ttk.Button(mainframe, text="Login", style='my.TButton', command=lambda: [parent.hide_frame(LandingPage), parent.show_frame(LoginPage)])
        login_button.grid(column=0, row=2, sticky="nsew")

        register_label = ttk.Label(mainframe, text="If you're a first time user, click here to create an account:")
        register_label.grid(column=0, row=3, sticky="w", pady=(20,5))
        register_label.config(font=('Times', 16))
        register_button = ttk.Button(mainframe, text="Create an account", style='my.TButton', command=lambda: [parent.hide_frame(LandingPage), parent.show_frame(RegisterPage)])
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

        back_button = ttk.Button(self, text='Back', style='my.TButton', command= lambda: [parent.hide_frame(LoginPage), self.email_entry.delete(0, END), self.password_entry.delete(0, END), parent.show_frame(LandingPage)])
        back_button.grid(column=0, row=2, sticky="sw")

        login_frame = ttk.Frame(self)
        login_frame.grid(column=1, row=1)
        login_frame.grid_rowconfigure(0, weight=1)
        login_frame.grid_columnconfigure(0, weight=1)

        email_label = ttk.Label(login_frame, text="Email:", font=('Times', 16))
        email_label.grid(column=0, row=0, sticky="nsew", padx=(0, 10), pady=(0,10))

        email = StringVar()
        self.email_entry = ttk.Entry(login_frame, width=30, textvariable=email, font=('Times', 16))
        self.email_entry.grid(column=1, row=0, sticky="w", pady=(0,10))

        password_label = ttk.Label(login_frame, text="Password:", font=('Times', 16))
        password_label.grid(column=0, row=1, sticky="nsew", pady=(0,10))

        password = StringVar()
        self.password_entry = ttk.Entry(login_frame, width=30, textvariable=password, show="*", font=('Times', 16))
        self.password_entry.grid(column=1, row=1, sticky="w", pady=(0,10))

        self.toggle_button = ttk.Button(login_frame, text='Show Password', style='my.TButton', width=15, command= lambda: self.toggle_password())
        self.toggle_button.grid(column=2, row=1, sticky="nw")

        login_button = ttk.Button(login_frame, text="Login", style='my.TButton', command= lambda: [self.login(email, password, parent)])
        login_button.grid(column=1, row=2, sticky="e")

        self.error_message = StringVar()
        error_message_label = ttk.Label(login_frame, font=('Times', 16), foreground='red', textvariable=self.error_message)
        error_message_label.grid(column=1, row=3, sticky="w")

    def login(self, email, password, parent):
        self.error_message.set('')
        try:
            user = parent.auth.sign_in_with_email_and_password(email.get(), password.get())
            parent.user_id = user['localId']
            parent.hide_frame(LoginPage)
            self.email_entry.delete(0, END)
            self.password_entry.delete(0, END)
            home_page = parent.frames[parent.HomePage]
            home_page.add_user(parent)
            parent.show_frame(parent.HomePage)
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

        back_button = ttk.Button(self, text='Back', style='my.TButton', command= lambda: [parent.hide_frame(RegisterPage), self.email_entry.delete(0, END), self.password_entry.delete(0, END), self.error_message.set(''), self.email_message.set(''), self.password_message.set(''), parent.show_frame(LandingPage)])
        back_button.grid(column=0, row=2, sticky="sw")

        register_frame = ttk.Frame(self)
        register_frame.grid(column=1, row=1)
        register_frame.grid_rowconfigure(0, weight=1)
        register_frame.grid_columnconfigure(0, weight=1)

        email_label = ttk.Label(register_frame, text="Email:", font=('Times', 16))
        email_label.grid(column=0, row=0, sticky="nsew", padx=(0, 10), pady=(0,10))

        email = StringVar()
        email.trace('w', self.check_both)
        self.email_entry = ttk.Entry(register_frame, width=30, textvariable=email, validate='focusout', validatecommand=check_email_wrapper, font=('Times', 16))
        self.email_entry.grid(column=1, row=0, sticky="w", pady=(0,10))

        self.email_message = StringVar()
        email_message = ttk.Label(register_frame, foreground='red', textvariable=self.email_message, font=('Times', 16))
        email_message.grid(column=1, row=1, sticky="nw")

        password_label = ttk.Label(register_frame, text="Password:", font=('Times', 16))
        password_label.grid(column=0, row=2, sticky="nsew", pady=(0,10))

        password = StringVar()
        password.trace('w', self.check_both)
        self.password_entry = ttk.Entry(register_frame, width=30, textvariable=password, show="*", validate='focusout', validatecommand=check_password_wrapper, font=('Times', 16))
        self.password_entry.grid(column=1, row=2, sticky="w", pady=(0,10))
        
        self.password_message = StringVar()
        password_message_label = ttk.Label(register_frame, foreground='red', textvariable=self.password_message, font=('Times', 16))
        password_message_label.grid(column=1, row=3, sticky="nw")

        self.toggle_button = ttk.Button(register_frame, text='Show Password', style='my.TButton', width=15, command= lambda: self.toggle_password())
        self.toggle_button.grid(column=2, row=2, sticky="nw")

        self.register_button = ttk.Button(register_frame, text="Register", style='my.TButton', command= lambda: [self.register_user(email, password, parent)])
        self.register_button.grid(column=1, row=4, sticky="e")
        self.register_button.state(['disabled'])

        self.error_message = StringVar()
        self.error_message_label = ttk.Label(register_frame, foreground='red', textvariable=self.error_message, font=('Times', 16))
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
        valid = re.match("\A(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)\Z", value) is not None
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