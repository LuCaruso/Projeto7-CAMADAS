#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time

# Tabela DTMF
DTMF_TABLE = {
    (697, 1209): '1',
    (697, 1336): '2',
    (697, 1477): '3',
    (770, 1209): '4',
    (770, 1336): '5',
    (770, 1477): '6',
    (852, 1209): '7',
    (852, 1336): '8',
    (852, 1477): '9',
    (941, 1336): '0'
}

#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    # Configurações de gravação
    freqDeAmostragem = 44100
    numCanais = 1

    #***instruções****
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = freqDeAmostragem #taxa de amostragem
    sd.default.channels = numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    tempo = 2 # tempo em segundos que ira aquisitar o sinal acustico captado pelo mic em segundos
    
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    numAmostras = freqDeAmostragem * tempo
    #faca um print na tela dizendo que a captacao comecará em n segundos. e entao 

    #use um time.sleep para a espera
    print("A captura 3 segundos...")
    print("\n")
    time.sleep(3)

    #Ao seguir, faca um print informando que a gravacao foi inicializada
    print("-----------------------GRAVANDO----------------------")
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=numCanais)
    sd.wait()
    print("----------------------FIM-----------------------------------")
    print("\n\n\n")

    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    print("Audio: {}" .format(audio))
    print("\n")
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    dados = audio[:, 0]  # caso de multi-canal

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t = np.linspace(0, tempo, numAmostras, endpoint=False)

    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) . 
    plt.figure()
    plt.plot(t, dados)
    plt.title("Sinal do audio ")
    plt.xlabel("Tempo ")
    plt.ylabel("Amplitude")
    plt.show()

    ## Calcule e plote o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    # Fourier do sinal
    xf, yf = signal.calcFFT(dados, freqDeAmostragem)
    plt.figure()
    plt.plot(xf, yf)
    plt.title("SFourier")
    plt.xlabel("Frequência")
    plt.ylabel("Amplitude")
    plt.show()
    
    #agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    #Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.   
    # Comece com os valores:
    index = peakutils.indexes(yf, thres=0.2, min_dist=50)
    print("index de picos {}" .format(index)) #yf é o resultado da transformada de fourier
    print("\n")

    #printe os picos encontrados! 
    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito
    peaks = [xf[i] for i in index]


    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print o valor tecla!!!
    # Encontrar as frequências próximas e mapear para a tecla
    found_freqs = sorted([round(p) for p in peaks if p < 1500])[:2]
    tecla = DTMF_TABLE.get(tuple(found_freqs), "Não reconhecida")
    print(f"Tecla pressionada: {tecla}")
    
    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

if __name__ == "__main__":
    main()