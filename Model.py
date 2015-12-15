#!usr/env/bin python

"""
The Model used for the application. The Controller class
primarily calls the Router class which serves as a proxy to the Model.

"""


import librosa as lsa


class Model(object):

    def __init__(self, wavefile_path=None):     # set to None to allow pickle-load

        self.__data = {
            'raw': None,
            'fs': None,
            'stft': None,
            'mel': None,
            'const_q': None,
            'onset': None
        }

        if wavefile_path is not None:                   # if not pickle-load


            self.wavefile = wavefile_path
            self.__compute_raw()
            self.__compute_const_q()
            self.__compute_mel()
            self.__compute_onset()
            self.__compute_stft()

        print "Model initialized"

    def __compute_raw(self):
        self.__data['raw'], self.__data['fs'] = lsa.load(self.wavefile, sr=44100)

    def __compute_stft(self):

        stft = lsa.stft(self.__data['raw'])
        self.__data['stft'] = lsa.logamplitude(stft)

    def __compute_mel(self):
        sr = self.__data['fs']
        spec = lsa.feature.melspectrogram(self.__data['raw'], sr=sr, n_fft=1024)

        self.__data['mel'] = lsa.logamplitude(spec)

    def __compute_const_q(self):
        sr = self.__data['fs']
        fmin = lsa.midi_to_hz(48)
        const = lsa.feature.chroma_cqt(self.__data['raw'], sr=sr, fmin=fmin)

        self.__data['const_q'] = lsa.logamplitude(const)

    def __compute_onset(self):
        sr = self.__data['fs']
        self.__data['onset'] = lsa.onset.onset_detect(self.__data['raw'], sr=sr)


    #getters for each
    def get_raw(self):
        return self.__data['raw']

    def get_sr(self):
        return self.__data['fs']

    def get_stft(self):
        return self.__data['stft']

    def get_mel(self):
        return self.__data['mel']

    def get_const_q(self):
        return self.__data['const_q']

    def get_onset(self):
        return self.__data['onset']

    # getter for object
    def get_all_data(self):
        return self.__data

    # setter for object -- for pickle load in controller
    def set_all_data(self, data_obj):
        self.__data = data_obj


class Router(object):

    """
    Proxy router for controller -- initialized after Model() in controller class
    communicates between controller.fetch_data and model
    """

    def __init__(self, model):
        self.model = model

    def request(self, obj_name):

        req = {
            'raw': self.model.get_raw,
            'stft': self.model.get_stft,
            'fs': self.model.get_sr,
            'mel': self.model.get_mel,
            'const_q': self.model.get_const_q,
            'onset': self.model.get_onset,
            'all': self.model.get_all_data
        }

        return req[obj_name]()
