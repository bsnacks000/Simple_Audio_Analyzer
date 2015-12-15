#!usr/env/bin python

"""
Controller class for the application

"""

import Tkinter as tk
import tkFileDialog
import tkMessageBox
import librosa as lsa

import json
import pickle
import os
import webbrowser

from Model import Model, Router
from Views import StartView, TopMenu, WaveView, MelView, ConstqView, OnsetView


class Controller(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.model = None
        self.router = None
        self.frames = {}

        # Build main Window

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Build menu

        menubar_parent = tk.Menu(self)
        menubar = TopMenu(menubar_parent, self)

        # make StartView -- only shown on program init

        start = StartView(self.container, self)
        self.frames['StartView'] = start
        self.show_frame('StartView')

    def show_frame(self, container_name):

        frame = self.frames[container_name]
        frame.tkraise()

    def load_session(self):
        """
        Loads session... builds View dictionary and Router; fetches data needed for plots
        """
        wavefile_path = tkFileDialog.askopenfilename(filetypes=[('Wave', '*.wav')])

        try:
            self.model = Model(wavefile_path)

        except (EOFError, lsa.LibrosaError, lsa.ParameterError):
                message = "Sorry, Simple Audio Analyzer cannot open this .wav file. File is corrupt " \
                          "or contains incorrect data"
                tkMessageBox.showerror("File Error",message=message)

        self.router = Router(self.model)

        self.__build_frames()
        self.show_frame('WaveView')

    def export_data(self):

        """
        exports and saves a JSON file.
        """

        data = self.fetch_data('all')

        for k, i in data.iteritems():    # convert to normal list for json
            if 'numpy' in str(type(i)):
                data[k] = data[k].tolist()

        filename = tkFileDialog.asksaveasfilename(defaultextension='.json')

        with open(filename, 'w') as outfile:
            json.dump(data, outfile)

    def save_object(self):

        """
        Pickles the data object from Model and saves as a .sesh file

        """

        data = self.fetch_data('all')

        # only saves and loads  *.sesh files
        filename = tkFileDialog.asksaveasfilename(defaultextension='.sesh', filetypes=[('Session', '*.sesh')])

        with open(filename, 'w') as outfile:
            pickle.dump(data, outfile)
            print "Session stored: " + os.path.realpath(filename)

    def load_object(self):

        """
        Loads the data from a .sesh picklecached object. Handles file errors.

        """

        filename = tkFileDialog.askopenfilename(defaultextension='.sesh', filetypes=[('Session', '*.sesh')])

        with open(filename, 'r') as infile:

            try:
                data = pickle.load(infile)
                self.model = Model()               # create a new Model & Router
                self.router = Router(self.model)
                self.model.set_all_data(data)      # set model data

            except Exception:
                message = "There was an error loading the .sesh file. Object data is either corrupt" \
                          " or improperly formatted."
                tkMessageBox.showerror("Load Error", message=message)

            self.__build_frames()              # build the frames and show
            self.show_frame('WaveView')

    def fetch_data(self, data_key_name):    # data key name as string
        """
        possible strings: all, raw, const_q, onset, mel, stft
        """
        # probably needs some error handling either here or in the router

        return self.router.request(data_key_name)

    def exit(self):
        """
        gracefully exit via file menu
        """
        self.quit()

    def about(self):

        """
        displays the About Message Box
        """
        about_message = """

        written by J.DeBlase, 2015...This application is free to download use and share.\n

        Special thanks to the development team at librosa and Stanford MIR.

        """

        tkMessageBox.showinfo("Analysis Help", about_message)

    def help(self):
        """
        displays the github Readme page
        """
        try:
            webbrowser.open("https://github.com/bsnacks000/Simple_Audio_Analyzer", new=2)

        except webbrowser.Error:

            message = "Browser Control Error: Could not connect to README.md"
            tkMessageBox.showerror("Browser Error", message=message)

    def __build_frames(self):

        for View in (WaveView, MelView, ConstqView, OnsetView):  # build views AFTER model/router is built

            frame = View(self.container, self)
            self.frames[frame.__repr__()] = frame
            frame.grid(row=0, column=0, sticky="nsew")


