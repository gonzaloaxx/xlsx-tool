#!usr/bin/python3
#-*- coding: utf-8 -*-

from tkinter import Toplevel, Listbox, Scrollbar

class TkPreview(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)

        self.title("Previsualizacion")
        self.config(padx=10, pady=10, bg='#FFF')
        self.geometry('400x300')
        self.resizable(True, True)

        self.bind('<Escape>', lambda x: self.destroy())
        self.bind('<Return>', lambda x: self.destroy())

        self.preview = Listbox(self)
        self.scrollbar = Scrollbar(self, orient='vertical')
        self.scrollbar.pack(side='right', fill='y')
        self.preview.configure(background='#FFF',
                               foreground='#2C2C2C',
                               selectbackground='#2C2C2C',
                               selectforeground='#FFF',
                               selectmode='browse',
                               yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.preview.yview)
        self.preview.pack(fill='both', expand='yes')
    


    def insert_reg(self, string:str):
        self.preview.insert('end', string)