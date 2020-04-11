import csv

import matplotlib
from matplotlib import ticker

matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import *
import numpy as np


data = []
with open('exchange_rate.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)


class SwitchGraphs:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.config_window()
        self.graph_id = 0
        self.days()

    def config_window(self):
        toolbar = NavigationToolbar2Tk(self.canvas, self.master)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)
        b_day = Button(self.master, text="Days", command=self.days)
        b_day.pack(side=BOTTOM)
        b_week = Button(self.master, text="Weeks", command=self.weeks)
        b_week.pack(side=BOTTOM)
        b_months = Button(self.master, text="Months", command=self.months)
        b_months.pack(side=BOTTOM)
        b_years = Button(self.master, text="Years", command=self.years)
        b_years.pack(side=BOTTOM)

    def set_axes(self):
        self.figure.axes[0].get_xaxis().set_major_locator(ticker.LinearLocator(numticks=11))
        self.figure.axes[0].get_xaxis().set_ticklabels(np.arange(2010, 2021, step=1))

    def days(self):
        self.ax.cla()
        self.set_axes()
        usd = []
        for item in data:
            usd.append(float(item.get('USD')))
        self.ax.plot(usd)
        self.canvas.draw()

    def weeks(self):
        self.ax.cla()
        self.set_axes()
        k = 0
        avg = 0
        usd = []
        for i, item in enumerate(data):
            k += 1
            avg += float(item.get('USD'))
            if k == 7 or i == len(data) - 1:
                usd.append(avg/k)
                avg = 0
                k = 0
        self.ax.plot(usd)
        self.canvas.draw()

    def months(self):
        self.ax.cla()
        self.set_axes()
        k = 0
        avg = 0
        usd = []
        for i in range(len(data)-1):
            k += 1
            avg += float(data[i].get('USD'))
            if data[i+1].get('date')[3:5] != data[i].get('date')[3:5]:
                usd.append(avg/k)
        self.ax.plot(usd)
        self.canvas.draw()

    def years(self):
        self.ax.cla()
        k = 0
        avg = 0
        usd = []
        date = np.arange(2010, 2021, step=1)
        for i in range(len(data) - 1):
            k += 1
            avg += float(data[i].get('USD'))
            if data[i + 1].get('date')[-4:] != data[i].get('date')[-4:] or i == len(data) - 2:
                usd.append(avg / k)
        self.ax.plot(date, usd)
        self.canvas.draw()


root = Tk()
SwitchGraphs(root)
root.mainloop()
