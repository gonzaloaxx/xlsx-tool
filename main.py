#!usr/bin/python3
#-*- coding: utf-8 -*-

from lib.qtApplication import QtApplication
from lib.popups import getOpenFiles
from lib.coreutils import createDataFrame
from lib.coreutils import listCsvFiles
from lib.coreutils import getValuesFromString
from lib.coreutils import searchValuesOnCsv
from lib.coreutils import getCsvHeaders


class Main():

    def __init__(self) -> None:
        self.qtApp = QtApplication()
        self.localDir = '.local'
        self.localFilenames = []
    

    def searchEvent(self):
        # obtener valores desde el input
        inputValues = self.qtApp.getSearchInput()
        filteredValues = getValuesFromString(inputValues)

        # obtener ruta del archivo elegido en la interfaz
        currentFilename = self.qtApp.getCurrentFile()

        # busqueda principal de valores en dataset precargado
        try:
            matches, notMatches = searchValuesOnCsv(
                searchValues=filteredValues,
                fileDir=self.localDir,
                fileName=currentFilename
            )
        except FileNotFoundError:
            statusMessage = 'No hay archivos cargados para cotejar con los datos'
            self.qtApp.setStatus(message=statusMessage)
            return

        # actualizar mensaje del sistema
        statusMessage = 'Buscados:%s - Encontrados:%s - No encontrados:%s'
        statusMessage = statusMessage % (
            len(filteredValues),len(matches),len(notMatches)
        )
        self.qtApp.setStatus(message=statusMessage)


        # presentacion en interfaz de resultados encontrados
        csvHeaders = getCsvHeaders(self.localDir, currentFilename)
        self.qtApp.setMatchesHeaders(csvHeaders)
        self.qtApp.setMatchesRows(*matches)

        # presentacion en interfaz de resultados no encontrados        
        self.qtApp.setNotMatchesRows(*notMatches)

    def openFiles(self):
        self.localFilenames = []

        # actualizar mensajes de sistema
        statusMessage = 'Cargar archivos Excel'
        self.qtApp.setStatus(message=statusMessage)

        filenames = getOpenFiles()
        if len(filenames):
            progressCount = 0
            progressStep = 100 // len(filenames)

            for i in filenames:
                try:
                    localFilePath = createDataFrame(i, self.localDir)
                except:
                    statusMessage = 'Ocurrio un error al cargar archivo'
                    self.qtApp.setStatus(message=statusMessage)

                else:
                    self.localFilenames.append(localFilePath)
                    filename = i.split('/')[-1]
                    statusMessage = 'Archivo cargado correctamente: %s' % filename
                    self.qtApp.setStatus(message=statusMessage)

                    # barra de progreso
                    self.qtApp.uiMainWindow.progressBar.show()
                    progressCount = progressCount + progressStep
                    self.qtApp.uiMainWindow.progressBar.setValue(progressCount)

        else:
            statusMessage = 'No se seleccionaron archivos para cargar'
            self.qtApp.setStatus(message=statusMessage)
            return
        
        self.qtApp.uiMainWindow.progressBar.hide() # ocultar barra de progreso

        statusMessage = 'Se cargaron correctamente %s archivos' % len(self.localFilenames)
        self.qtApp.setStatus(message=statusMessage)
        self.loadLocalFiles()




    def loadLocalFiles(self):
        # se busca en archivos locales para construir combobox
        cachedFiles = listCsvFiles(self.localDir)
        self.qtApp.setComboBoxItems(*cachedFiles)



    def execute(self):
        self.qtApp.uiMainWindow.btSearch.clicked.connect(self.searchEvent)
        self.qtApp.uiMainWindow.btOpenFile.clicked.connect(self.openFiles)

        self.loadLocalFiles()
        
        self.qtApp.appBuilder()
        exit(self.qtApp.exec_())



if __name__ == '__main__':
    app = Main()
    app.execute()