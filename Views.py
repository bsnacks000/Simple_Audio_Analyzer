#!usr/env/bin python

"""
All Views for the Application

"""


import Tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import librosa as lsa


class StartView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


    def __repr__(self):
        return 'StartView'


class TopMenu(tk.Menu):

    def __init__(self, parent, controller):
        tk.Menu.__init__(self, parent)

        menubar = tk.Menu(parent)

        filemenu = tk.Menu(menubar)
        filemenu.add_command(label="Load New File", command=controller.load_session)   # add callbacks just like buttons
        filemenu.add_command(label="Load Session", command=controller.load_object)
        filemenu.add_command(label="Save Session", command=controller.save_object)
        filemenu.add_command(label="Export JSON", command=controller.export_data)
        filemenu.add_command(label="Quit", command=controller.exit)

        # cascade packs into menubar
        menubar.add_cascade(label="File", menu=filemenu)

        # here's another menu for Help
        helpmenu = tk.Menu(menubar)
        helpmenu.add_command(label="About", command=controller.about)
        helpmenu.add_command(label="Help", command=controller.help)

        menubar.add_cascade(label="Help", menu=helpmenu)
        controller.config(menu=menubar)


### ONE VIEW PER GRAPH -- WaveView, StftView, MelView,ConstqView. OnsetView


class WaveView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Waveplot')
        label.pack(side=tk.TOP)

        prev_plot = tk.Button(self, text='<--Prev Plot', command=lambda: controller.show_frame('OnsetView'))
        prev_plot.pack(side=tk.BOTTOM)

        next_plot = tk.Button(self, text='Next Plot-->', command=lambda: controller.show_frame('MelView'))
        next_plot.pack(side=tk.TOP)

        ## call fetch data for plots
        plt.style.use('ggplot')

        wave = controller.fetch_data('raw')
        sr = controller.fetch_data('fs')

        fig = plt.figure(figsize=(10,10), dpi=100)   # make figure
        fig.add_subplot(111)
        lsa.display.waveplot(wave, sr, alpha=0.75, x_axis='time')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack(side=tk.TOP, expand=True)

    def __repr__(self):
        return 'WaveView'


class MelView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Mel Plot')
        label.pack(side=tk.TOP)

        prev_plot = tk.Button(self, text='<--Prev Plot', command=lambda: controller.show_frame('WaveView'))
        prev_plot.pack(side=tk.BOTTOM)

        next_plot = tk.Button(self, text='Next Plot-->', command=lambda: controller.show_frame('ConstqView'))
        next_plot.pack(side=tk.TOP)
        plt.style.use('ggplot')

        mel = controller.fetch_data('mel')
        sr = controller.fetch_data('fs')

        fig = plt.figure(figsize=(10,10), dpi=100)   # make figure
        fig.add_subplot(111)
        lsa.display.specshow(mel, sr, x_axis='time',  y_axis='mel')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack(side=tk.TOP, expand=True)

    def __repr__(self):
        return 'MelView'


class ConstqView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Constant-Q Plot')
        label.pack(side=tk.TOP)

        prev_plot = tk.Button(self, text='<--Prev Plot', command=lambda: controller.show_frame('MelView'))
        prev_plot.pack(side=tk.BOTTOM)

        next_plot = tk.Button(self, text='Next Plot-->', command=lambda: controller.show_frame('OnsetView'))
        next_plot.pack(side=tk.TOP)

        ## call fetch data for plots
        plt.style.use('ggplot')

        c = controller.fetch_data('const_q')

        fig = plt.figure(figsize=(10,10), dpi=100)   # make figure
        fig.add_subplot(111)

        fmin = lsa.midi_to_hz(48)
        lsa.display.specshow(c, x_axis='time', y_axis='cqt_note', fmin=fmin, cmap='coolwarm')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack(side=tk.TOP, expand=True)

    def __repr__(self):
        return 'ConstqView'


class OnsetView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Onset Detection/STFT Plot')
        label.pack(side=tk.TOP)

        prev_plot = tk.Button(self, text='<--Prev Plot', command=lambda: controller.show_frame('ConstqView'))
        prev_plot.pack(side=tk.BOTTOM)

        next_plot = tk.Button(self, text='Next Plot-->', command=lambda: controller.show_frame('WaveView'))
        next_plot.pack(side=tk.TOP)

        ## call fetch data for plots
        plt.style.use('ggplot')

        ons = controller.fetch_data('onset')
        stft = controller.fetch_data('stft')
        sr = controller.fetch_data('fs')

        fig = plt.figure(figsize=(10,10), dpi=100)   # make figure
        fig.add_subplot(111)

        lsa.display.specshow(stft, sr=sr, alpha=0.75, x_axis='time', y_axis='mel')
        plt.vlines(ons, 0, stft.shape[0], color='r')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack(side=tk.TOP, expand=True)

    def __repr__(self):
        return 'OnsetView'
