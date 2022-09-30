from tkinter import *
import customtkinter
from tkinter.ttk import Progressbar
from linearity.record_audio import record
import numpy as np
from linearity.linearity import linealidad
import pandas as pd
import os
from linearity.linearity import RMS_cal
import time

cwd = os.getcwd()
os.chdir(cwd)

global my_entries

my_entries = []

def calcular():
    """Una vez obtenidos los audios, paso a calcular linealidad"""
    global cal
    global data
    global sr
    global progress_label
    global root

    progress.set(0)
    progress_label.set("Calculando...")
    root.update_idletasks()

    auricular = tipo_auricular.get()

    test = linealidad(cal, data, sr, auricular)

    file_name = file_name_entry.get()

    """
    writer = pd.ExcelWriter(f'{file_name}.xlsx', engine='xlsxwriter')

    workbook  = writer.book

    bg_color = ['#C71C05', '#CF6F0F', '#EFC439', '#EFE55F', '#A6EB29', '#31A711', '#15A34E',
                '#15C1AD', '#107498', '#242CD2', '#8C23D3', '#D75FC0', '#D75F65']
    
    cols = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']

    columns = ['40 dBHL', '37.5 dBHL', '35 dBHL', '32.5 dBHL', '30 dBHL', '27.5 dBHL', '25 dBHL', '22.5 dBHL',
               '20 dBHL', '17.5 dBHL', '15 dBHL', '12.5 dBHL', '10 dBHL']

    levels = [40, 37.5, 35, 32.5, 30, 27.5, 25, 22.5, 20, 17.5, 15, 12.5, 10]

    for i, key in enumerate(test.keys()):
        test[key].to_excel(writer, sheet_name=key)

        worksheet = writer.sheets[key]

        for c, col in enumerate(columns):
            worksheet.conditional_format(f'{cols[c]}1', {'type': 'cell',
                                         'criteria': '==',
                                         'value': col,
                                         'format': workbook.add_format({'bg_color': bg_color[c]})})

        for c, level in enumerate(levels):
            worksheet.conditional_format('B2:N7', {'type': 'cell',
                                         'criteria': 'between',
                                         'minimum': level - 0.5,
                                         'maximum': level + 0.5,
                                         'format': workbook.add_format({'bg_color': bg_color[c]})})
    

    writer.save()
    """

    writer = pd.ExcelWriter(f'{file_name}.xlsx', engine='xlsxwriter')

    for key in test.keys():
        test[key].to_excel(writer, sheet_name=key)

    writer.save()
    
    progress_label.set("Valores guardados!")
    root.update_idletasks()

    

def record_cal():
    """Grabar calibración para baja ganancia"""
    global cal #Defino la calibración como variable global
    global progress_label
    global root
    
    freqs = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
    supraural_comp = [45, 27, 13.5, 9, 7.5, 7.5, 9, 11.5, 12, 16, 15.5]
    circumaural_comp = [30.5, 18, 11, 6,  5.5, 5.5, 4.5, 2.5, 9.5, 17, 17.5]
    auricular = tipo_auricular.get()
    bar = 0
    cal = []

    if auricular == 'Supraural (ej: JBL600)':
        comp = supraural_comp #Compensación para supraural
    elif auricular == "Circumaural (ej: JBL750)":
        comp = circumaural_comp #Compensación para circumaural
    else:
        raise TypeError("No cargaste ningún auricular")

    for i, freq in enumerate(freqs):
    
        progress.set(bar)
        progress_label.set(f"Esperando calibración {freq} Hz")
        root.update_idletasks()

        cal_record, _ = record(RECORD_SECONDS=2) #Grabo la calibración
        rms_1Pa = RMS_cal(cal_record, nivel_dBHL=65, comp=comp[i])

        cal.append(rms_1Pa)

        progress_label.set(f"Grabado!")
        root.update_idletasks()
        time.sleep(5)

        if bar < 1:
            bar += 0.1
    
    progress.set(1)
    progress_label.set("Calibraciones cargadas!")
    root.update_idletasks()
    print('Calibraciones cargadas!')

def record_data():
    global data
    global sr
    global progress_label
    global root

    progress_label.set("")
    root.update_idletasks()
    progress.set(0.1)
    progress_label.set("Grabando el test")
    root.update_idletasks()

    # La variable record_seconds va a tener que ser 2*Cantidad_De_Pasos_En_Cada_Frecuencia
    record_seconds = 78*2 # [saltos_de_nivel]*[segundos_por_paso]
                          # [125,250...,8000]*[ 2[s] ]

    cant_de_frecuencias = 11
    print(f'Se grabaran {record_seconds*cant_de_frecuencias} [s] de audio')

    progress.set(0.15)
    root.update_idletasks()
    #progress.pack()

    freq = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]

    data = np.array([])

    for i in range(cant_de_frecuencias):
        print(f'Frecuencia a grabar: {freq[i]} Hz')
        data_aux, sr = record(RECORD_SECONDS=record_seconds)
        print(f'Se grabaron {len(data_aux)} muestras en esta iteración')

        print(f'Grabado {freq[i]} Hz')
        data = np.append(data, data_aux)
        print(f'Se acumularon {len(data)} muestras')

    #data = data[:int(11*2*11)]

    progress.set(1)
    progress_label.set("Test finalizado!")
    root.update_idletasks()

    print('Audio grabado!')

global root

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

root = customtkinter.CTk()
root.title("Test de linealidad")
root.geometry("300x380")
root.iconbitmap('logo.ico')

recomendacion0 = customtkinter.CTkLabel(root, text='Seleccione el tipo de auricular:')
recomendacion0.grid(row=0, column=0, pady=5, padx=50)
tipo_auricular = customtkinter.CTkOptionMenu(root, values=["Supraural (ej: JBL600)", "Circumaural (ej: JBL750)"])
tipo_auricular.grid(row=2, column=0, pady=5, padx=50)
tipo_auricular.set("Supraural (ej: JBL600)")

recomendacion1 = customtkinter.CTkLabel(root, text='Recomendado: 1 kHz @ 65 dBHL')
recomendacion1.grid(row=4, column=0, pady=5, padx=50)

cal_low = customtkinter.CTkButton(root, text="Calibración", command=record_cal)
cal_low.grid(row=5, column=0, pady=5, padx=50)

record_low = customtkinter.CTkButton(root, text="Grabar test", command=record_data)
record_low.grid(row=6, column=0, pady=5, padx=50)

global progress_label
progress_label = StringVar()
progress_label.set("")
recomendacion2 = customtkinter.CTkLabel(root, textvariable=progress_label)
recomendacion2.grid(row=7, column=0, pady=5, padx=50)

progress = customtkinter.CTkProgressBar(root)
progress.grid(row=8, column=0, pady=5, padx=50)
progress.set(0)

file_name_recomendacion = customtkinter.CTkLabel(root, text='Nombre del archivo:')
file_name_recomendacion.grid(row=9, column=0, pady=5, padx=50)

file_name_entry = customtkinter.CTkEntry(root, justify=LEFT, textvariable='Nombre del excel')
file_name_entry.grid(row=10, column=0, pady=5, padx=50)

calculate = customtkinter.CTkButton(root, text="Calcular", command=calcular)
calculate.grid(row=11, column=0, pady=5, padx=50)

root.mainloop()