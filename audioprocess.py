import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt
import time, sys
import tkinter as tk
import scipy.fftpack as fourier
from pygame import mixer
from tkinter import filedialog
from scipy.signal import butter, lfilter, freqz, decimate, buttord

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
def plotting(sig, modSig, demodSig, n):
    fig, ax = plt.subplots(3, 1)
    ax[0].plot(n,sig)
    ax[0].set_xlabel('Time')
    ax[0].set_ylabel('Amplitude')
    ax[1].plot(n,modSig,'g') 
    ax[1].set_xlabel('Modulated Signal')
    ax[2].plot(n,demodSig, 'r')
    ax[2].set_xlabel('Demodulated Signal')
    plt.show()

def passafaixa(h1, Fs2):
    # Filtro Passa-Faixa
    gpass= 3 # Ripple na banda de passagem
    gstop= 40 # Atenuação na banda de rejeição
    fp1= 13000# Frequências de corte
    fp2=2000
    fs1=1000 # Frequências de rejeição
    fs2=0
    fn = Fs2/2 # Frequência de Nyquist
    Wp1=fp1/fn # Frequências normalizada
    Wp2=fp2/fn
    Ws1=fs1/fn
    Ws2=fs2/fn

    a = abs(np.fft.fftshift(np.fft.fft(h1)))
    a = a[int(len(a)/2):len(a)-1]
    freqs = np.fft.fftfreq(len(a))
    order, Wc = buttord([Wp1, Wp2], [Ws1, Ws2], gpass, gstop)
    B, A = butter(order, Wc, btype='bandpass', fs=Fs2)
    filtered_signal = lfilter(B, A, h1, axis=0)
    w, h = freqz(B, A)
    print(Wp1)
    print(Wp2)
    print(Ws1)
    print(Ws2)
    print(Wc)

    fig, ax1 = plt.subplots()
    #plt.plot(freqs, a,  color='green')
    ax1.set_title('Digital filter frequency response')
    ax1.set_ylabel('Amplitude [dB]', color='b')
    ax1.set_xlabel('Frequency [rad/sample]')
    ax1.plot(w, 20 * np.log10(abs(h)), 'b')
    ax2 = ax1.twinx()
    #angles = np.unwrap(np.angle(h))
    ax2.plot(freqs, a, 'g')
    ax2.set_ylabel('', color='g')

    #plt.figure(figsize=(12, 4))
    #plt.title('Sinal Filtrado')
    #plt.xlabel('Tempo(s)')
    #plt.ylabel('Amplitude')
    #plt.plot(n2, y)

def modula(carrier, sig):
    mod = carrier * sig
    return mod

def demodula(sig, mult):
    demod = sig * mult
    return demod

# Dá play no som
sound = mixer.Sound(file_path)
sound.play()
time.sleep(2)

(freq,sig) = wav.read(file_path)
Fs = freq
audlength = len(sig)/freq
n = np.arange(0, audlength, 1/Fs)
Fc = 100 #Frequência do Carrier
Ac = 1 #Amplitude do Carrier

mult = np.cos(2*np.pi*Fc*n + np.pi/2)
factor = int(input("Escreva o fator de dizimação:"))

carrier = Ac * mult
sig = decimate(sig, factor)
modulatedSig = modula(carrier, sig)
demodulatedSig = demodula(modulatedSig, mult)

plotting(sig, modulatedSig, demodulatedSig, n)