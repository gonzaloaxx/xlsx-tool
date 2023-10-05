#!usr/bin/python3
#-*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QKeySequence
from lib.mainwindow import Ui_MainWindow

class QtApplication(QApplication):
    def __init__(self):
        super().__init__([])

        self.qMainWindow = QMainWindow()
        self.uiMainWindow = Ui_MainWindow()
        self.uiMainWindow.setupUi(self.qMainWindow)
        self.app_version_file = 'version.txt'

        # inicio de ventana maximizado
        self.qMainWindow.showMaximized()

        # el titulo de la ventana se concatena con el numero de version
        windowName = self.qMainWindow.windowTitle()
        try:
            with open(self.app_version_file) as vfile:
                appVersion = vfile.read()
        except: pass
        else: self.qMainWindow.setWindowTitle('%s v%s' % (windowName, appVersion))


        self.uiMainWindow.progressBar.hide() # ocultar barra de progreso
        
        # reset a la tabla de resultados vacia
        self.uiMainWindow.matchesTable.setColumnCount(0)
        self.uiMainWindow.matchesTable.setRowCount(0)

        # vaciar la lista de resultados no encontrados
        self.uiMainWindow.notMatchList.clear()

        # vaciar elementos del combo box
        self.uiMainWindow.selectFile.clear()

        # creacion hotkeys
        self.hotkey0 = QShortcut(QKeySequence('Ctrl+q'), self.qMainWindow)
        self.hotkey0.activated.connect(self.quit)

        self.hotkey1 = QShortcut(QKeySequence('Ctrl+f'), self.qMainWindow)
        self.hotkey1.activated.connect(self.focusOnSearchHotkey)

        self.hotkey2 = QShortcut(QKeySequence('Return'), self.qMainWindow)
        self.hotkey2.activated.connect(self.searchEventHotkey)



    def searchEventHotkey(self):
        if self.uiMainWindow.searchEntry.hasFocus():
            self.uiMainWindow.btSearch.click()

       
    def focusOnSearchHotkey(self):
        self.uiMainWindow.searchEntry.selectAll()
        self.uiMainWindow.searchEntry.setFocus()


    def getSearchInput(self):
        return self.uiMainWindow.searchEntry.text()
    

    def setStatus(self, message:str):
        self.uiMainWindow.statusLabel.setText(message)
    

    def setComboBoxItems(self, *items):
        self.uiMainWindow.selectFile.clear()
        
        for i in items:
            self.uiMainWindow.selectFile.addItem(i)


    def getCurrentFile(self):
        return self.uiMainWindow.selectFile.currentText()
    


    def setMatchesHeaders(self, *headers):
        self.uiMainWindow.matchesTable.clear()
        self.uiMainWindow.matchesTable.setColumnCount(len(*headers))
        self.uiMainWindow.matchesTable.setHorizontalHeaderLabels(*headers)
    


    def setMatchesRows(self, *rows):
        self.uiMainWindow.matchesTable.setRowCount(0)

        for rowIndex, rowData in enumerate(rows):
            self.uiMainWindow.matchesTable.insertRow(rowIndex)

            for columnIndex, columnData in enumerate(rowData):
                item = QTableWidgetItem(columnData)
                self.uiMainWindow.matchesTable.setItem(rowIndex, columnIndex, item)
    

    def setNotMatchesRows(self, *rows):
        self.uiMainWindow.notMatchList.clear()
        for i in rows:
            self.uiMainWindow.notMatchList.addItem(i)


    def appBuilder(self):
        self.qMainWindow.show()