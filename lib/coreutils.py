#!usr/bin/python3
#-*- coding: utf-8 -*-

from os import path, mkdir, listdir, remove
from pandas import DataFrame
from pandas import read_excel
from pandas import concat
from re import findall
from csv import reader

def localDir(pathDir:str):
    if not path.isdir(pathDir):
        mkdir(pathDir)


def isExcelFile(filePath:str) ->bool:
    extension = filePath.split('.')[-1]
    return extension == 'xlsx'


def isCsvFile(filePath:str) ->bool:
    extension = filePath.split('.')[-1]
    return extension == 'csv'



def listCsvFiles(pathDir:str):
    localDir(pathDir=pathDir)
    files = listdir(pathDir)
    csvFiles = [x for x in files if isCsvFile(x)]
    return csvFiles



def createDataFrame(sourceFile:str, outputDir:str)->str:
    # Si el archivo no existe, crear un DataFrame vacío
    dfCsv = DataFrame()

    if isExcelFile(sourceFile):
        # comprobar la existencia del directorio contenedor
        localDir(outputDir)

        # Leer el archivo Excel sin incluir los encabezados
        dfExcel = read_excel(sourceFile)

        # Agregar una columna con nombre de archivo correspondiente
        filename = sourceFile.split('/')[-1]
        dfExcel['Archivo'] = filename

        # Agregar las filas del archivo Excel al DataFrame del CSV
        dfCsv = concat([dfCsv, dfExcel])

        # Guardar el DataFrame resultante en el archivo CSV
        filePath = path.join(outputDir, '%s.csv' %filename)
        dfCsv.to_csv(filePath, index=False, encoding='utf-8')
    
    else: return False
    return filePath



def getValuesFromString(text:str) ->list:
    # Utilizar expresión regular para buscar palabras
    values = findall(r'(?:(?<!\\)[\t\n\r\\]+|[^\t\n\r\\]+)', text)    
    filteredValues = [x for x in set(values) if not '\n' in x]
    return filteredValues



def searchValuesOnCsv(searchValues:iter, fileDir:str, fileName:str):
    # ruta relativa al archivo
    filepath = path.join(fileDir, fileName)

    searchValues = [x.lower() for x in searchValues]
    matches = [] # inicializacion resultados encontrados    
    notMatches = [] # inicializacion resultados no encontrados

    with open(filepath, encoding='utf-8') as sourceFile:
        csvReader = reader(sourceFile)

        # buscar los registros que aparecen
        for reg in csvReader:
            for value in reg:
                if value.lower() in searchValues:
                    matches.append(reg)

    # buscar valores que no aparecen en la lista matches
    for value in searchValues:
        flag = False
        for reg in matches:
            if value in reg:
                flag = True
                break
        if flag: flag = False
        else: notMatches.append(value)
    

    return matches, notMatches


def getCsvHeaders(fileDir:str, fileName:str):
    filepath = path.join(fileDir, fileName)

    with open(filepath, encoding='utf-8') as sourceFile:
        csvReader = reader(sourceFile)
        return csvReader.__next__()
    

def deleteFiles(pathDir:str):
    files = listCsvFiles(pathDir=pathDir)
    for i in files: remove(path.join(pathDir, i))
    return files