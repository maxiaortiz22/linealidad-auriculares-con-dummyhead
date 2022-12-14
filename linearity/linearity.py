import numpy as np
import pandas as pd
import sys
from scipy.fft import rfft, rfftfreq

#Recomendable: calibrar con un tono de 65 dBHL a 1kHz


def RMS(y):
    """ Calcula el valor RMS de una señal """
    rms = np.sqrt(np.mean(y**2))
    #rms=np.mean(y**2)
    return rms

def RMS_cal(y, nivel_dBHL, comp):
    """ Calcula el valor RMS de una señal de calibración de cualquier nivel y lo paso a 94 dBSPL,
        lo que equivale a 1 Pa """

    rms = np.sqrt(np.mean(y**2)) #Obento el RMS al nivel que fue grabado

    rms_1Pa = rms / (20*10**(-6) * 10**((nivel_dBHL+comp)/20)) #Paso le RMS a 1 Pa
    
    return rms_1Pa

def linealidad(cal, data, sr, auricular):
    """Esta función hace el cálculo de linealidad. Primero todo todo el audio grabado y lo
    separo por banda sabiendo cuánto dura la grabación de cada una. Después de eso hago todo el
    calculo de linealidad. Luego tengo que saber cuánto es el máximo y el mínimo de nivel medido
    para crear el cuadro de linealidad"""

    #calibration = RMS_cal(y=cal, nivel_dBHL=65, auricular=auricular) # Lo dejo para 65 dBHL (testear esto)

    frec = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000] #Frequencies to analyze

    #Creo diccionarios con los audios grabados, la key de cada diccionario es la frecuencia grabada
    audios = {}
    
    i=0
    recorte = int(78*2*sr) #[pasos][segundos_grabacion][sr] = [muestras_por_frecuencia] no sera 12?
    for cal_i, f in enumerate(frec):
        #Separo la data por frecuencia y los calibro a dBSPL:
        audios[str(f)] = data[int(i) : int(i + recorte)] / cal[cal_i] #calibration

        i+=recorte

    
    #Recorto los audios en partes de dos segundos
    i=0
    trimm = {}
    for key in audios.keys():
        n_cut = round(len(audios[key])/(sr*2),0) #cantidad de cortes
        #print(n_cut)
        cut = int(len(audios[key])/n_cut)
        for t in range(0,int(n_cut)):
            i+=1
            trimm[key+'_'+str(i)] = audios[key][int(cut*t) : int(cut*(t+1))] #recorte de dos segundos
            trimm[key+'_'+str(i)] = trimm[key+'_'+str(i)][int(0.5*sr) : int(-0.5*sr)] #testear si funciona
                                                                                      #mejor con este recorte
        i=0

    trimm_global_dB = {'125': [],
                       '250': [],
                       '500': [],
                       '750': [],
                       '1000': [],
                       '1500': [],
                       '2000': [],
                       '3000': [], 
                       '4000': [],
                       '6000': [],
                       '8000': []}

    for key in trimm.keys(): #Guardo el valor de la fft

        # Number of samples in normalized_tone
        N = len(trimm[key])

        # Note the extra 'r' at the front
        yf = np.abs(rfft(trimm[key])) / (N/np.sqrt(2)) #Divido por N/raiz(2) para compensar la amplitud de la fft
        xf = rfftfreq(N, 1 / sr)

        yf_db = 20*np.log10(yf / (20*10**(-6)) + sys.float_info.epsilon)

        idx = np.where(xf == int(key.split('_')[0]))[0]

        trimm_global_dB[key.split('_')[0]].append(yf_db[idx])


    supraural_comp = {'125': 45,
                      '250': 27,
                      '500': 13.5,
                      '750': 9,
                      '1000': 7.5,
                      '1500': 7.5,
                      '2000': 9,
                      '3000': 11.5, 
                      '4000': 12,
                      '6000': 16,
                      '8000': 15.5}

    circumaural_comp = {'125': 30.5,
                        '250': 18,
                        '500': 11,
                        '750': 6,
                        '1000': 5.5,
                        '1500': 5.5,
                        '2000': 4.5,
                        '3000': 2.5, 
                        '4000': 9.5,
                        '6000': 17,
                        '8000': 17.5}


    trimm_global_dB_norm = {}
    aux = []
    for key in trimm_global_dB.keys():
        if auricular == 'Supraural (ej: JBL600)':
            for i in range(len(trimm_global_dB[key])):
                aux.append(np.round_(trimm_global_dB[key][i] - supraural_comp[key])[0])
            trimm_global_dB_norm[key+'Hz'] = aux
        elif auricular == "Circumaural (ej: JBL750)":
            for i in range(len(trimm_global_dB[key])):
                aux.append(np.round_(trimm_global_dB[key][i] - circumaural_comp[key])[0])
            trimm_global_dB_norm[key+'Hz'] = aux
        else:
            raise TypeError("No cargaste ningún auricular")
        
        aux = []

    columns = ['40 dBHL', '37.5 dBHL', '35 dBHL', '32.5 dBHL', '30 dBHL', '27.5 dBHL', '25 dBHL', '22.5 dBHL',
               '20 dBHL', '17.5 dBHL', '15 dBHL', '12.5 dBHL', '10 dBHL']

    INDEX = ['15 Gain', '14 Gain', '13 Gain', '12 Gain', '11 Gain', '10 Gain']

    df_dict = {}
    aux_dic = {}
    i=0
    for key in trimm_global_dB_norm.keys():
        for t in range(int(len(trimm_global_dB_norm[key])/len(INDEX))):

            #assert len(columns) == int(len(trimm_global_dB_norm[key])/len(INDEX))

            aux_dic[columns[t]] = trimm_global_dB_norm[key][i:(i+len(INDEX))]
            print(aux_dic)
            i+=len(INDEX)

        df_dict[key] = pd.DataFrame(data=aux_dic, index=INDEX)
        aux_dic = {}
        i=0     

    #test = pd.DataFrame(data=trimm_global_dB_norm, index=INDEX)

    print(df_dict)

    return df_dict