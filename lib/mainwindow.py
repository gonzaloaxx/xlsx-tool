#!usr/bin/python3
#-*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QKeySequence
from uic.ui_mainwindow import Ui_MainWindow

class MainWindow(QApplication):
    def __init__(self):
        super().__init__([])
        self.setStyle('Fusion')

        self.q_mainwindow = QMainWindow()
        self.ui_mainwindow = Ui_MainWindow()
        self.ui_mainwindow.setupUi(self.q_mainwindow)

        # inicio de ventana maximizado
        self.q_mainwindow.showMaximized()
        self.ui_mainwindow.progressbar.hide() # ocultar barra de progreso
        
        # creacion hotkeys
        self.bind0 = QShortcut(QKeySequence('Ctrl+q'), self.q_mainwindow)
        self.bind0.activated.connect(self.quit)
        self.bind1 = QShortcut(QKeySequence('Ctrl+f'), self.q_mainwindow)
        self.bind1.activated.connect(self.focus_search_bind)
        self.bind2 = QShortcut(QKeySequence('Return'), self.q_mainwindow)
        self.bind2.activated.connect(self.search_bind)
        self.bind2 = QShortcut(QKeySequence('Ctrl+c'), self.q_mainwindow)
        self.bind2.activated.connect(self.copy_bind)


    def copy_bind(self):
        clipboard = QApplication.clipboard()
        clipboard.clear()
        
        if self.ui_mainwindow.notmatch_list.hasFocus():
            selected_indexes = self.ui_mainwindow.notmatch_list.selectedIndexes()
            if selected_indexes:
                selected_rows = list(set(index.row() for index in selected_indexes))
                selected_cols = list(set(index.column() for index in selected_indexes))
                
                copied_data = []
                for row in selected_rows:
                    row_data = []
                    for col in selected_cols:
                        item = self.ui_mainwindow.notmatch_list.item(row)
                        if item:
                            row_data.append(item.text())
                        
                        else:
                            row_data.append('')
                    copied_data.append('\t'.join(row_data))
                clipboard.setText('\n'.join(copied_data))
        
        elif self.ui_mainwindow.match_table.hasFocus():
            selected_indexes = self.ui_mainwindow.match_table.selectedIndexes()
            if selected_indexes:
                selected_rows = list(set(index.row() for index in selected_indexes))
                selected_cols = list(set(index.column() for index in selected_indexes))
                
                copied_data = []
                for row in selected_rows:
                    row_data = []
                    for col in selected_cols:
                        item = self.ui_mainwindow.match_table.item(row, col)
                        if item:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    copied_data.append('; '.join(row_data))
                clipboard.setText('\n'.join(copied_data))


    def search_bind(self):
        if self.ui_mainwindow.search_entry.hasFocus():
            self.ui_mainwindow.search_button.click()
       

    def focus_search_bind(self):
        self.ui_mainwindow.search_entry.selectAll()
        self.ui_mainwindow.search_entry.setFocus()


    def get_search_input(self):
        return self.ui_mainwindow.search_entry.text()
    
    
    def set_status(self, message:str):
        self.ui_mainwindow.status_label.setText(message)
    

    def set_combobox_items(self, *items):
        self.ui_mainwindow.selectfile_button.clear()
        
        for i in items:
            self.ui_mainwindow.selectfile_button.addItem(i)


    def get_currentfile(self):
        return self.ui_mainwindow.selectfile_button.currentText()
    

    def set_match_table_headers(self, *headers):
        self.ui_mainwindow.match_table.clear()
        self.ui_mainwindow.match_table.setColumnCount(len(*headers))
        self.ui_mainwindow.match_table.setHorizontalHeaderLabels(*headers)


    def insert_match(self, *rows):
        self.ui_mainwindow.match_table.setRowCount(0)

        for row_index, row_data in enumerate(rows):
            self.ui_mainwindow.match_table.insertRow(row_index)

            for column_index, column_data in enumerate(row_data):
                item = QTableWidgetItem(column_data)
                self.ui_mainwindow.match_table.setItem(row_index, column_index, item)
    

    def insert_notmatch(self, *rows):
        self.ui_mainwindow.notmatch_list.clear()
        for i in rows:
            self.ui_mainwindow.notmatch_list.addItem(i)
