#!usr/bin/python3
#-*- coding: utf-8 -*-

from os import path, mkdir, listdir, remove
from pandas import DataFrame
from pandas import read_excel
from pandas import concat
from re import findall
from csv import reader
from PyQt5.QtWidgets import QFileDialog


def get_openfiles():
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly

    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.ExistingFiles)

    files, _ = dialog.getOpenFileNames(
        dialog, 'Archivos Excel', '', 'Archivos (*.xlsx *.xls)',
        options=options)
    
    return files

def check_localdir(dirpath:str):
    if not path.isdir(dirpath):
        mkdir(dirpath)


def is_xlsx_file(filepath:str) ->bool:
    extension = filepath.split('.')[-1]
    return extension == 'xlsx'


def is_csv_file(filepath:str) ->bool:
    extension = filepath.split('.')[-1]
    return extension == 'csv'



def get_local_csvfiles(dirpath:str) ->list:
    check_localdir(dirpath=dirpath)
    files = listdir(dirpath)
    csvFiles = [x for x in files if is_csv_file(x)]
    return csvFiles



def create_dataframe(sourceFile:str, outputDir:str)->str:
    # Si el archivo no existe, crear un DataFrame vacío
    dfCsv = DataFrame()

    if is_xlsx_file(sourceFile):
        # comprobar la existencia del directorio contenedor
        check_localdir(outputDir)

        # Leer el archivo Excel sin incluir los encabezados
        dfExcel = read_excel(sourceFile)

        # Agregar una columna con nombre de archivo correspondiente
        filename = sourceFile.split('/')[-1]
        dfExcel['Archivo'] = filename

        # Agregar las filas del archivo Excel al DataFrame del CSV
        dfCsv = concat([dfCsv, dfExcel])

        # Guardar el DataFrame resultante en el archivo CSV
        filepath = path.join(outputDir, '%s.csv' %filename)
        dfCsv.to_csv(filepath, index=False, encoding='utf-8')
    
    else: return False
    return filepath



def get_values_from_string(text:str) ->list:
    # Utilizar expresión regular para buscar palabras
    values = findall(r'(?:(?<!\\)[\t\n\r\\]+|[^\t\n\r\\]+)', text)    
    filteredValues = [x for x in set(values) if not '\n' in x]
    return filteredValues



def search_values_on_csv(search_values:iter, csv_dir:str, csv_filename:str):
    # ruta relativa al archivo
    filepath = path.join(csv_dir, csv_filename)

    search_values = [x.lower() for x in search_values]
    match = [] # inicializacion resultados encontrados    
    not_match = [] # inicializacion resultados no encontrados

    with open(filepath, encoding='utf-8') as csvfile:
        csv_reader = reader(csvfile)

        # buscar los registros que aparecen
        for reg in csv_reader:
            for value in reg:
                if value.lower() in search_values:
                    match.append(reg)

    # buscar valores que no aparecen en la lista match
    for value in search_values:
        flag = False
        for reg in match:
            if value in reg:
                flag = True
                break
        if flag: flag = False
        else: not_match.append(value)
    
    return match, not_match


def get_csv_headers(csv_dir:str, csv_filename:str):
    filepath = path.join(csv_dir, csv_filename)

    with open(filepath, encoding='utf-8') as sourceFile:
        csv_reader = reader(sourceFile)
        return csv_reader.__next__()
    

def delete_localfiles(dirpath:str):
    files = get_local_csvfiles(dirpath=dirpath)
    for i in files: remove(path.join(dirpath, i))
    return files