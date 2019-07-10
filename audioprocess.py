import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt
import sys
import tkinter as tk
import scipy.fftpack as fourier
from tkinter import filedialog
from scipy.signal import butter, lfilter, freqz, decimate, buttord, resample

def plotting(sig, modSig, n):
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(n,sig)
    ax[0].set_xlabel('Time')
    ax[0].set_ylabel('Amplitude')
    ax[1].plot(n,modSig,'g') 
    ax[1].set_xlabel('Modulated Signal')
    plt.show()
"""
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
"""
def modula(carrier, sig):
    mod = carrier * sig
    return mod

def demodula(sig, carrier):
    demod = sig * carrier
    return demod

#Inicializando
root = tk.Tk()
file_path = filedialog.askopenfilename()

(freq,sig) = wav.read(file_path)
Fs = freq
audlength = len(sig)/freq
n1 = np.arange(0, audlength/2, 1/Fs)
Fc = 5000 #Frequência do Carrier
Ac = 1 #Amplitude do Carrier

mult = np.cos(2*np.pi*Fc*n1 + np.pi/2)
factor = int(input("Escreva o fator de dizimação:"))

carrier = (Ac * mult)
"""Gráfico do sinal Carrier
plt.title('Sinal Portador')
plt.plot(n, carrier)
plt.grid()
plt.show()
"""
sig = decimate(sig, factor)
modulatedSig = modula(carrier, sig)
plotting(sig, modulatedSig, n1) #Plota o primeiro sinal e a sua versão modulada

print("==Segundo arquivo==")
file_path = filedialog.askopenfilename()
(freq, sig2) = wav.read(file_path)
Fs = freq
audlength = len(sig2)/freq
n2 = np.arange(0, audlength/2, 1/Fs)

mult = np.cos(2*np.pi*Fc*n2 + np.pi/2)
carrier = (Ac * mult)
"""Gráfico do sinal Carrier
plt.title('Sinal Portador')
plt.plot(n, carrier)
plt.grid()
plt.show()
"""

sig2 = decimate(sig2, factor)
modulatedSig2 = modula(carrier, sig2)

plotting(sig2, modulatedSig2, n2)

#Iguala o comprimento dos sinais, cortando o 'resto' do maior
if len(sig) > len(sig2):
    modulatedSig = modulatedSig[:len(modulatedSig2)]
    n1 = n2
if len(sig) < len(sig2):
    modulatedSig2 = modulatedSig2[:len(modulatedSig)]
    n2 = n1

#Soma os sinais modulados
modulatedSig = modulatedSig + modulatedSig2
mult = np.cos(2*np.pi*Fc*n2 + np.pi/2)
carrier = (Ac * mult)

demodulatedSig = demodula(modulatedSig, carrier)
plt.plot(n1, demodulatedSig)
plt.title('Sinal demodulado')
plt.xlabel('n')
plt.ylabel('Amplitude')
plt.show()

#Upsampling do sinal
resample(demodulatedSig, len(sig))
wav.write('./audios/demodsig.wav', Fs, demodulatedSig)