#!usr/bin/python3
#-*- coding: utf-8 -*-

from tkinter.filedialog import askopenfilenames
from tkinter.messagebox import askyesno


def get_openfilenames() ->tuple:
        return askopenfilenames(
            title='Archivos Excel',
            filetypes=[('Excel', '*xlsx')]
        )


def askme_loadfiles() ->bool:
        return askyesno(
                title='Archivos Excel',
                message='Se van a cargar archivos. ¿Esta seguro?',
        )