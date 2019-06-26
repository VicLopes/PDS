import sys
import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt
import time, sys
from pygame import mixer


def to_mono(filename, canal=0):
    """
    Abre arquivo wav e retorna como estéreo
    :parâmetro filename: file name
    :parâmetro canal: índice do canal
    :return: tupla de frequência e dados em array do numpy
    """
    (freq, sig) = wav.read(filename)
    if sig.ndim == 2:
        return (sig[:,canal], freq)
    return (sig, freq)


def cut(dados, freq, start, end):
    """
    :parâmetro track: dados do áudio wav
    :parâmetro start: início (em segundos)
    :parâmetro end: fim (em segundos)
    :parâmetro freq: frequência dos dados de áudio
    :return: áudio cortado
    """
    end = int(end*freq)
    if end > len(dados):
        return dados[int(start*freq):]
    return dados[int(start*freq):end]


def seconds(dados, freq):
    """
    Retorna quantos segundos tem a música de acordo com a frequência
    :parâmetro track: dados do arquivo wav
    :parâmetro freq: frequência dos dados de áudio
    :return: número de segundos
    """
    return len(dados)/freq


def process(dados, callback=None):
    """
    Pode modificar o sinal de áudio com a função 'callback' aplicada a todo frame de dados
    Ou simplesmente retorna a cópia do próprio áudio caso o callback seja 'None'
    :parâmetro dados: dados do arquivo .wav
    :return: cópia do áudio com as modificações caso necessário
    """
    if not callback:
        def callback(t):
            return t
    output = np.empty(shape=[len(dados)], dtype=np.int16)
    for i in xrange(0, len(dados)):
        output.put(i, callback(dados[i]))
    return output

#Utilidade


def save(filename, dados, freq):
    """
    Contém o método write para simplificação do código caso necessário usar
    :parâmetro filename: nome do arquivo wav
    :parâmetro freq: frequência dos dados de áudio
    :parâmetro dados: dados do arquivo wav
    """
    wav.write(filename=filename, rate=freq, dados=dados)

#Desenha os dados


def espectrograma(dados, freq, NFFT=256, noverlap=128, mode='psd', sides='default'):
    """
    Desenha o espectrograma do arquivo de áudio com os dados do arquivo de áudio utilizando o método specgram do matplotlib
    Argumentos mínimos são os dados de áudio e a frequência
    :parâmetro dados: dados do áudio em wav
    :parâmetro freq: frequência dos dados de áudio
    :return: ver a documentação matplotlib.specgram - primeiro parâmetro é matplotlib.pyplot
    """
    sec = seconds(dados, freq)
    xtick = np.linspace(0, sec, num=len(dados))
    plt.plot(xtick, dados)          #plota os dados de amplitude do áudio
    return (plt)


if __name__ == '__main__':
    print("Desenhará o espectrograma do arquivo de áudio especificado: ex. python process.py test.wav")
    if len(sys.argv) == 2:
        mixer.init()
        sound = mixer.Sound(sys.argv[1])
        sound.play()
        time.sleep(10)   
        espectrograma(*to_mono(sys.argv[1]))[0].show()