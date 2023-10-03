#!usr/bin/python3
#-*- coding: utf-8 -*-

from PyQt5.QtWidgets import QFileDialog


def getOpenFiles():
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly

    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.ExistingFiles)

    files, _ = dialog.getOpenFileNames(
        dialog, 'Archivos Excel', '', 'Archivos (*.xlsx *.xls)',
        options=options)
    
    return files