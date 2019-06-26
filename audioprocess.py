import numpy as np
import wave, struct, math
import matplotlib.pyplot as plt
import time, sys
import tkinter as tk
from tkinter import filedialog
from pygame import mixer


root = tk.Tk()
file_path = filedialog.askopenfilename()
adb = wave.open(file_path, 'r') # Abre arquivo do áudio

def modula():
    amsc = wave.open("/audios/amsc.wav", 'w')
    am = wave.open("/audios/am.wav", 'w')
    carrier = wave.open("/audios/carrier.wav", 'w')

    for n in (am, amsc, carrier):
        n.setchannels(1)
        n.setsampwidth(2)
        n.setframerate(44100)

    for n in range(0, adb.getnframes()):
        base = struct.unpack('h', adb.readframes(1))[0] / 32768.0
        carrier_sample = math.cos(3000.0 * (n / 44100.0) * math.pi * 2) # Gera um carrier de 3000 Hz

        signal_am = signal_amsc = base*carrier_sample
        signal_am += carrier_sample
        signal_am /= 2
        
        amsc.writeframes(struct.pack('h', signal_amsc * 32768)) # gera um am_sc pq eu quero
        am.writeframes(struct.pack('h', signal_am * 32768)) # gera o am que queremos
        carrier.writeframes(struct.pack('h', carrier_sample * 32768))

def demodula():
    modulated = wave.open("/audios/am.wav", 'r')

    f = demod_am = wave.open("/audios/demod_am.wav", 'w')
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(44100)

    for n in range(0, modulated.getnframes()):
        signal = struct.unpack('h', modulated.readframes(1))[0] / 32768.0
        signal = abs(signal)
        demod_am.writeframes(struct.pack('h', signal * 32767))
        

mixer.init()
sound = mixer.Sound(file_path)
sound.play() # Toca o som dj

modula()
demodula()

mod_am = wave.open("/audios/am.wav", 'r')
demod_am = wave.open("/audios/demod_am.wav", 'r')

signal = adb.readframes(-1)
signal = np.fromstring(signal, 'Int16') # Transforma o sinal em um numero para ser plotado no futuro
fs = adb.getframerate() # Obtem a taxa de amostragem do sinal

#Se for Stereo
if adb.getnchannels() == 2:
    print('Utilize arquivos mono apenas!')
    sys.exit(0)

signaltime = np.linspace(0, len(signal)/fs, num=len(signal))

fig, ax = plt.subplots(3,1)

#Plota o audio original
ax[0].plot(signaltime, signal)
ax[0].title('Audio original')
ax[0].set_xlabel('Tempo')
ax[0].set_ylabel('Amplitude')

#Plota o audio modulado
signal = mod_am.readframes(-1)
signal = np.fromstring(signal, 'Int16')
ax[1].plot(signaltime, signal)
ax[1].title('Audio modulado')
ax[1].set_xlabel('Tempo')
ax[1].set_ylabel('Amplitude')

#Plota o audio demodulado
signal = demod_am.readframes(-1)
signal = np.fromstring(signal, 'Int16')
ax[2].plot(signaltime, signal)
ax[2].title('Audio demodulado')
ax[2].set_xlabel('Tempo')
ax[2].set_ylabel('Amplitude')

plt.show()