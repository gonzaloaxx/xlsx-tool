#!usr/bin/python3
#-*- coding: utf-8 -*-

from pandas import read_excel, DataFrame, concat
from csv import reader
from re import findall

LOCALFILENAME = '.application'


def is_excel_file(filepath:str) ->bool:
    extension = filepath.split('.')[-1]
    return extension == 'xlsx'



def create_dataframe(excel_files:iter, output_filename:str)->int:
    # Si el archivo no existe, crear un DataFrame vacío
    df_csv = DataFrame()

    # Recorrer la lista de archivos Excel
    loaded_files = 0
    for excel in excel_files:
        if is_excel_file(excel):
            # Leer el archivo Excel sin incluir los encabezados
            df_excel = read_excel(excel, header=None)

            # Agregar una columna con nombre de archivo correspondiente
            filename = excel.split('/')[-1]
            df_excel['archivo'] = filename

            # Agregar las filas del archivo Excel al DataFrame del CSV
            df_csv = concat([df_csv, df_excel], ignore_index=True)
        loaded_files += 1

    # Guardar el DataFrame resultante en el archivo CSV
    df_csv.to_csv(LOCALFILENAME, index=False, encoding='utf-8')
    return loaded_files




def get_values_from_string(text:str) ->tuple:
    # Utilizar expresión regular para buscar palabras
    values = findall(r'(?:(?<!\\)[\t\n\r\\]+|[^\t\n\r\\]+)', text)    
    filtered_values = [x for x in set(values) if not '\n' in x]
    return filtered_values




def search_values_in_csv(values_to_search:iter):
    # inicializar la lista de resultados encontrados
    matches = []
    # inicializar la lista de resultados no encontrados
    not_matches = []


    with open(LOCALFILENAME, encoding='utf-8') as source_file:
        csv_reader = reader(source_file)

        # buscar los registros que aparecen
        for reg in csv_reader:
            for value in reg:
                if value in values_to_search:
                    matches.append(reg)

    # buscar valores que no aparecen en la lista matches
    for value in values_to_search:
        flag = False
        for reg in matches:
            if value in reg:
                flag = True
                break
        if flag: flag = False
        else: not_matches.append(value)
    

    return matches, not_matches