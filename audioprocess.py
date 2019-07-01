import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt
import time, sys
import tkinter as tk
import scipy.fftpack as fourier
from pygame import mixer
from tkinter import filedialog
from scipy.signal import butter, lfilter, freqz

#Inicializando
root = tk.Tk()
file_path = filedialog.askopenfilename()
mixer.init()

"""
class Filter(object):
    def __init__(self, cutoff):
        self.cutoff_frequency = cutoff
    
    def LPF(self, n):
        time = n
    """
def plotting(sig, modSig, demodSig):
    fig, ax = plt.subplots(3, 1)
    ax[0].plot(n,sig)
    ax[0].set_xlabel('Time')
    ax[0].set_ylabel('Amplitude')
    ax[1].plot(n,modSig,'g') 
    ax[1].set_xlabel('Carrier')
    ax[2].plot(n,demodSig, 'r')
    ax[2].set_xlabel('Modulated Signal')
    plt.show()

# Dá play no som
sound = mixer.Sound(file_path)
sound.play()
time.sleep(2)

(freq,sig) = wav.read(file_path)
Fs = freq
audlength = len(sig)/freq
n = np.arange(0, audlength, 1/Fs)
Fc = 88000
Ac = 3

carrier = Ac*np.cos(2*np.pi*Fc*n)
modulatedSig = carrier*sig
demodulatedSig = modulatedSig * Ac*np.cos(2*np.pi*3*n)

plotting(sig, modulatedSig, demodulatedSig)
