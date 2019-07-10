import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt
import sys
import tkinter as tk
import scipy.fftpack as fourier
import sklearn.metrics as metrics
from tkinter import filedialog
from scipy.signal import butter, lfilter, freqz, decimate, buttord, resample, iirdesign

def plotting(sig, modSig, n):
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(n,sig)
    ax[0].set_xlabel('Time')
    ax[0].set_ylabel('Amplitude')
    ax[1].plot(n,modSig,'g') 
    ax[1].set_xlabel('Modulated Signal')
    plt.show()

def passafaixa(h1, Fs2):
    # Filtro Passa-Faixa
    gpass= 3 # Ripple na banda de passagem
    gstop= 82 # Atenuação na banda de rejeição
    fs1=9000 # Frequências de rejeição
    fp1= 11000# Frequências de corte
    fp2=13000
    fs2=14000
    fn = Fs2/2 # Frequência de Nyquist
    Wp1=fp1/fn  # Frequências normalizada
    Wp2=fp2/fn  
    Ws1=fs1/fn 
    Ws2=fs2/fn 

    a = abs(np.fft.fftshift(np.fft.fft(h1)))
    a = a[int(len(a)/2):len(a)-1]
    freqs = np.fft.fftfreq(len(a))
    order, Wc = buttord([Wp1, Wp2], [Ws1, Ws2], gpass, gstop)
    B, A = butter(order, Wc, btype='bandpass', fs=Fs2)
    B,A = iirdesign(wp = [0.2, 0.4], ws= [0.03, 0.6], gstop= gstop, gpass=gpass, ftype='butter')
    filtered_signal = lfilter(B, A, h1, axis=0)
    w, h = freqz(B, A)
    print(Wp1)
    print(Wp2)
    print(Ws1)
    print(Ws2)
    #print(Wc)
    #print(order/2)

    fig = plt.figure(figsize=(18,5))
    ax1 = fig.add_subplot(1, 1, 1)
    ax2 = ax1.twinx()
    t = np.linspace(0., 10., 100)
    ax1.plot(w, 20 * np.log10(abs(h)), 'b')
    ax2.plot(freqs, a, 'g')

    ax1.set_title('Digital filter frequency response')
    ax1.set_ylabel('Amplitude [dB]', color='b')
    ax1.set_xlabel('Frequency [rad/sample]')

    plt.plot(freqs, a,  color='green')

    #angles = np.unwrap(np.angle(h))

    ax2.set_ylabel('', color='g')

    #plt.figure(figsize=(12, 4))
    #plt.title('Sinal Filtrado')
    #plt.xlabel('Tempo(s)')
    #plt.ylabel('Amplitude')
    #plt.show()

    return filtered_signal

def modula(carrier, sig):
    mod = carrier * sig
    return mod

def demodula(sig, carrier):
    demod = sig * carrier
    return demod

#Inicializando
root = tk.Tk()
file_path1 = filedialog.askopenfilename()

(freq,sig) = wav.read(file_path1)
Fs = freq
audlength1 = len(sig)/freq
Fc = 5000 #Frequência do Carrier
Ac = 1 #Amplitude do Carrier


factor = int(input("Escreva o fator de dizimação:"))
n1 = np.arange(0, audlength1/factor, 1/Fs)
mult = np.cos(2*np.pi*Fc*n1 + np.pi/2)

carrier = (Ac * mult)
"""Gráfico do sinal Carrier
plt.title('Sinal Portador')
plt.plot(n, carrier)
plt.grid()
plt.show()
"""
decSig = decimate(sig, factor)
modulatedSig = modula(carrier, decSig)
plotting(decSig, modulatedSig, n1) #Plota o primeiro sinal e a sua versão modulada

print("==Segundo arquivo==")
file_path2 = filedialog.askopenfilename()
(freq, sig2) = wav.read(file_path2)
Fs = freq
audlength2 = len(sig2)/freq
n2 = np.arange(0, audlength2/factor, 1/Fs)

mult = np.cos(2*np.pi*Fc*n2 + np.pi/2)
carrier = (Ac * mult)
"""Gráfico do sinal Carrier
plt.title('Sinal Portador')
plt.plot(n, carrier)
plt.grid()
plt.show()
"""

decSig2 = decimate(sig2, factor)
modulatedSig2 = modula(carrier, decSig2)

plotting(decSig2, modulatedSig2, n2)

#Iguala o comprimento dos sinais, cortando o 'resto' do maior
if len(decSig) > len(decSig2):
    modulatedSig = modulatedSig[:len(modulatedSig2)]
    n1 = n2
    audlength1 = audlength2
if len(decSig) < len(decSig2):
    modulatedSig2 = modulatedSig2[:len(modulatedSig)]
    n2 = n1
    audlength2 = audlength1

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

passSig = passafaixa(demodulatedSig, Fs)

#Upsampling do sinal
passSig = resample(passSig, len(sig))

input("Aperte enter para continuar.")
plotting(sig, passSig, np.arange(0, audlength1, 1/Fs))

print(metrics.mean_squared_error(sig, passSig))