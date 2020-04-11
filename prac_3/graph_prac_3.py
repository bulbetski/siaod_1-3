import matplotlib
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

matplotlib.use('TkAgg')

import pandas as pd
from tkinter import *


# from wwo_hist import retrieve_hist_data
# frequency = 3
# start_date = '30-MAR-2010'
# end_date = '30-MAR-2020'
# api_key = '01b39d75e3d64c0384d193516200204'
# location_list = ['moscow']
# hist_weather_data = retrieve_hist_data(api_key,
#                                        location_list,
#                                        start_date,
#                                        end_date,
#                                        frequency,
#                                        location_label=False,
#                                        export_csv=True,
#                                        store_df=True)


class SwitchGraph:
    def __init__(self, master):
        self.df = pd.read_csv('moscow.csv')
        self.modified_df = self.df
        self.graph_id = 0
        self.start = StringVar()
        self.end = StringVar()
        self.master = master
        self.frame = Frame(self.master)
        self.figure = Figure(figsize=(16, 9), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.config_window()
        self.configure_df()
        self.days()

    def configure_df(self):
        self.modified_df = self.modified_df[['date_time', 'tempC']]
        self.modified_df['date_time'] = pd.to_datetime(self.modified_df['date_time'])
        self.modified_df = self.modified_df[self.modified_df['date_time'].dt.strftime('%H:%M:%S').between('09:00:00', '21:00:00')]
        self.modified_df.set_index('date_time', inplace=True, drop=True)
        self.modified_df = self.modified_df.groupby(self.modified_df.index.date).mean()

    def config_window(self):
        toolbar = NavigationToolbar2Tk(self.canvas, self.master)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)
        start_entry = Entry(textvariable=self.start)
        start_entry.pack()
        end_entry = Entry(textvariable=self.end)
        end_entry.pack()
        enter = Button(
            master=root,
            text='Enter',
            command=self.enter_pressed
        )
        enter.pack()
        b_day = Button(self.master, text="Days", command=self.days)
        b_day.pack(side=TOP)
        b_week = Button(self.master, text="Weeks", command=self.weeks)
        b_week.pack(side=TOP)
        b_months = Button(self.master, text="Months", command=self.months)
        b_months.pack(side=TOP)
        b_years = Button(self.master, text="Years", command=self.years)
        b_years.pack(side=TOP)

    def enter_pressed(self):
        func_array = [self.days, self.weeks, self.months, self.years]
        self.modified_df = self.df
        self.configure_df()
        self.modified_df = self.modified_df.reset_index().rename(columns={'index': 'date_time'})
        self.modified_df['date_time'] = pd.to_datetime(self.modified_df['date_time'])
        mask = (self.modified_df['date_time'] > pd.to_datetime(self.start.get())) & (self.modified_df['date_time'] <= pd.to_datetime(self.end.get()))
        self.modified_df = self.modified_df.loc[mask]
        self.modified_df.set_index('date_time', inplace=True, drop=True)
        self.modified_df = self.modified_df.groupby(self.modified_df.index.date).mean()
        func_array[self.graph_id]()

    def days(self):
        self.graph_id = 0
        self.ax.cla()
        self.ax.plot(self.modified_df.index, self.modified_df, label='avg temp')
        self.ax.legend()
        self.canvas.draw()

    def weeks(self):
        self.graph_id = 1
        self.ax.cla()
        rolling = self.modified_df.rolling(window=7).mean()
        self.ax.plot(rolling.index, rolling, label='avg temp')
        self.ax.legend()
        self.canvas.draw()

    def months(self):
        self.graph_id = 2
        self.ax.cla()
        rolling = self.modified_df.rolling(window=30).mean()

        self.ax.plot(rolling.index, rolling, label='avg temp')
        self.ax.legend()
        self.canvas.draw()

    def years(self):
        self.graph_id = 3
        self.ax.cla()
        rolling = self.modified_df.rolling(window=364).mean()
        self.ax.plot(rolling.index, rolling, label='avg temp')
        self.ax.legend()
        self.canvas.draw()


root = Tk()
SwitchGraph(root)
root.mainloop()




