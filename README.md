# Simple Audio Analyzer

A Tkinter application for Python 2.7 that wraps some of the feature extraction and functionality of `librosa` by Brian McFee

- Load a .wav file and view its waveform, mel-spectrogram,constant-q chromagram, beat onsets and stft
- Export the data as a JSON object for downstream analysis and machine learning applications.

## Installation

The application requires the `matplotlib` and `librosa`

The recommended installation is to clone this repo into a local directory and build a virtual environment. After activating the virtual environment use pip to install the application's dependencies.
    
    pip install -r requirements.txt
    
**NOTE** In order for librosa's plotting methods to work with `matplotlib >= 1.5` librosa needs to be updated to version 0.42. As of this publication pip only installs `librosa v0.41`. Therefore, after installing from requirements.txt, download and install `librosa v0.42` using `easy_install` as documented on <a href="https://github.com/bmcfee/librosa"> librosa's github page</a>. This can be done in the project directory.

    git clone https://github.com/bmcfee/librosa.git
    easy_install librosa


## Run

After installation, to run the application navigate to the source directory and run

    python main.py
    
If the project was built using a virtual environment make sure it is activated before running `main.py`


## Help/Functionality

**Load New File** - loads data from a new .wav file into a data dictionary of numpy arrays and draws plots <br>
  
  The four plots are:
  
  - *Wave Plot* - standard time-amplitude representation of the audio file
  - *Mel-Spectrogram* - representation of the short-term power spectrum based on linear cosine transform of a log power spectrum on a nonlinear mel scale of frequency
  - *Constant-Q Chromagram* - representation of the short-term power spectrum based with frequency transformed to pitch classes
  - *Onset/STFT* - short time fourier transform with onset markers 
  
**Export JSON** - exports the data dictionary to a JSON file for downstream use in other applications
**Save Session** - saves a the data dictionary object into a .sesh file
**Load Session** - loads the .sesh file and initializes the plots


