from tkinter import *
from tkinter import ttk
import pyrebase
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import datetime
from tkcalendar import DateEntry

global r_arrow_img, l_arrow_img

class StatsPage(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=6)
        self.rowconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        info_label = ttk.Label(self, text='Here you can view your overall stats or your day to day stats', wraplength=self.winfo_screenwidth()/2, font=('Times', 30))
        info_label.grid(column=0, row=0, columnspan=2)

        all_time_button = ttk.Button(self, text='Overall stats', style="my.TButton", command= lambda:[self.hide_frame(DailyStatsPage), self.show_frame(OverallStatsPage)])
        all_time_button.grid(column=0, row=1)

        daily_button = ttk.Button(self, text='Daily stats', style="my.TButton", command= lambda: [self.hide_frame(OverallStatsPage), self.show_frame(DailyStatsPage)])
        daily_button.grid(column=1, row=1)

        self.stats_frame = ttk.Frame(self)
        self.stats_frame.grid(row=2, column=0, columnspan=2)

        back_button = ttk.Button(self, text='Back', style="my.TButton", command= lambda: [parent.show_frame(parent.HomePage), self.destroy()])
        back_button.grid(column=0, row=3, sticky='sw')

        self.parent = parent

        self.frames = {}
        self.DailyStatsPage = DailyStatsPage
        self.OverallStatsPage = OverallStatsPage

        for F in {DailyStatsPage, OverallStatsPage}:
            self.init_frame(F)
            
        self.show_frame(OverallStatsPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.grid(row=0, column=0, sticky="nsew")

    def hide_frame(self, cont):
        frame = self.frames[cont]
        frame.grid_forget()

    def init_frame(self, F):
        frame = F(self.parent, self.stats_frame)
        self.frames[F] = frame

class OverallStatsPage(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=4)
        self.rowconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        try:
            df = pd.DataFrame.from_dict(parent.db.child("users").child(parent.user_id).child("results").get().val().values())
        except:
            label = ttk.Label(self, text="There aren't any completed exercises yet. Please complete an exercise and come back.", font=('Times', 23))
            label.grid(row=0, column=0)
            return
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].dt.date

        figure1 = plt.Figure(figsize=(6,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        stimuli_count = df.groupby('stimuli').size().values
        stimuli_labels = df.groupby('stimuli').groups.keys()
        ax1.pie(stimuli_count, labels=stimuli_labels)
        ax1.set_title('Number of exercises by type of stimuli')
        pie = FigureCanvasTkAgg(figure1, self)
        pie.get_tk_widget().grid(column=0, row=0, pady=(10,10), padx=(10,10))
        pie.get_tk_widget().config(relief='solid', borderwidth=2)

        figure2 = plt.Figure(figsize=(18,3), dpi=100)
        ax2 = figure2.add_subplot(111)
        dates = df.groupby('date').size()
        idx = pd.date_range(start=dates.keys()[0], end=dates.keys()[-1])
        new_dates = pd.DataFrame(dates)
        new_dates.index = pd.DatetimeIndex(dates.keys())
        new_dates = new_dates.reindex(idx, fill_value=0)
        ax2.plot(new_dates.index, new_dates[0])
        ax2.set_xlim(new_dates.index[0]-datetime.timedelta(days=1), new_dates.index[-1]+datetime.timedelta(days=1))
        ax2.xaxis.set_major_locator(md.DayLocator())
        ax2.xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
        ax2.set_title('Number of exercises by day')
        ax2.fmt_xdata = md.DateFormatter('%Y-%m-%d')
        figure2.autofmt_xdate()
        bar = FigureCanvasTkAgg(figure2, self)
        bar.get_tk_widget().grid(column=0, row=1, pady=(10,10), padx=(10,10), columnspan=2)
        bar.get_tk_widget().config(relief='solid', borderwidth=2)

        figure3 = plt.Figure(figsize=(8,5), dpi=100)
        ax3 = figure3.add_subplot(111)
        dates = df.groupby('date')['accuracy'].mean()
        ax3.scatter(x=np.arange(0, len(dates.keys()), 1), y=dates.values)
        ax3.set_xticks(np.arange(0, len(dates.keys()), 1), labels=np.array(dates.keys()))
        ax3.set_title('Average accuracy per day')
        figure3.autofmt_xdate()
        bar = FigureCanvasTkAgg(figure3, self)
        bar.get_tk_widget().grid(column=1, row=0, pady=(10,10), padx=(10,10))
        bar.get_tk_widget().config(relief='solid', borderwidth=2)
        

class DailyStatsPage(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        date = StringVar()
        self.date = ""
        global index
        index = 0

        try:
            self.df = pd.DataFrame.from_dict(parent.db.child("users").child(parent.user_id).child("results").get().val().values())
        except:
            stimuli_label.config(text="There aren't any completed exercises yet. Please complete an exercise and come back.")
            return
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['date'] = self.df['date'].dt.date

        def increase():
            global index
            index += 1

        def decrease():
            global index
            index =- 1

        def date_update():
            self.date = datetime.datetime.strptime(date.get(), '%m/%d/%y').date()
            global index
            index = 0
            show_results()

        def show_results():
            results = self.df[self.df['date'] == self.date]
            global index
            if index < 0:
                index = 0
            elif index >= len(results):
                index = len(results) - 1
            if(len(results)>0):
                stimuli_label.config(text=f'Practised stimuli: {results.iloc[index]["stimuli"]}')
                level_label.config(text=f'Difficulty level: {results.iloc[index]["level"]}')
                accuracy_label.config(text=f'Accuracy: {results.iloc[index]["accuracy"]}%')
                if(len(results)>1):
                    next_button.grid(row=2, column=2, pady=(20,0))
                    index_label.grid(row=2, column=1, pady=(20,0))
                    index_label.config(text=f'{index+1}')
                    prev_button.grid(row=2, column=0, pady=(20,0))
                else:
                    next_button.grid_forget()
                    prev_button.grid_forget()
                    index_label.grid_forget()
            else:
                next_button.grid_forget()
                prev_button.grid_forget()
                index_label.grid_forget()
                stimuli_label.config(text=f'No exercises exist for this date.')
                level_label.config(text=f'')
                accuracy_label.config(text=f'')
            return
            
        cal = DateEntry(self, selectmode='day', textvariable=date, year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)
        cal.grid(row=0, column=1, sticky='new')
        self.show_button = ttk.Button(self, text='Show', style="my.TButton", command=lambda:date_update())
        self.show_button.grid(row=1, column=1, pady=(10,0))

        stimuli_label = ttk.Label(self, text='', font=('Times', 23))
        stimuli_label.grid(row=3, column=0, columnspan=3, pady=(20,0))
        level_label = ttk.Label(self, text='', font=('Times', 23))
        level_label.grid(row=4, column=0, columnspan=3)
        accuracy_label = ttk.Label(self, text='', font=('Times', 23))
        accuracy_label.grid(row=5, column=0, columnspan=3)
        index_label = ttk.Label(self, text='', font=('Times', 18))

        self.r_arrow_img = PhotoImage(file='Images\\r_arrow.png')
        self.l_arrow_img = PhotoImage(file='Images\l_arrow.png')
        next_button = ttk.Button(self, image=self.r_arrow_img, command=lambda: [increase(), show_results()])
        prev_button = ttk.Button(self, image=self.l_arrow_img, command=lambda: [decrease(), show_results()])
        

    
        