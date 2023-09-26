#!usr/bin/python3
#-*- coding: utf-8 -*-

from base64 import b64decode
from configparser import ConfigParser
from tkinter import Entry, Tk
from tkinter import Frame
from tkinter import Label
from tkinter import Button
from tkinter import PhotoImage
from tkinter import Listbox
from tkinter import Scrollbar

class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        self.parser = ConfigParser()
        self.parser.read('application.ini')

        # contenedor ventana principal
        self.configure(padx=10, pady=5, background='#FFF')

        self.name = self.parser.get('application', 'name')
        self.version = self.parser.get('application', 'version')
        self.title('%s v-%s' % (self.name, self.version))

        win_width, win_height = 800, 500
        self.minsize(width=win_width, height=win_height)
        self.geometry('%sx%s' % (win_width, win_height))
        self.resizable(width=True, height=True)

        self.icon = PhotoImage(data=b64decode(self.parser.get('tk', 'png-icon')))
        self.iconphoto(True, self.icon)

        # cabecera de aplicacion
        self.div_header = Frame(self, bg='#2C2C2C')
        self.div_header.pack(fill='both')

        self.header = Label(self.div_header)
        self.header.config(
            background=self.header.master['background'],
            foreground='#FFF',
            text='Herramienta de busqueda en datasets y generacion de reportes'
        )
        self.header.pack(ipady=5)

        # seccion de busquedas
        self.div_search = Frame(self, bg='#FFF')
        self.div_search.pack(fill='both', padx=100, pady=20, ipady=2)

        ## caja de busquedas
        self.div_search_entry = Frame(self.div_search)
        self.div_search_entry.config(
            bg=self.div_search_entry.master['background']
        )
        self.div_search_entry.pack(side='left', fill='both', expand='yes')

        self.search_entry = Entry(self.div_search_entry)
        self.search_entry.config(
            border=1, borderwidth=1,
            background=self.search_entry.master['background'],
            foreground='#2C2C2C',
            selectbackground='#2C2C2C',
            selectforeground=self.search_entry.master['background'],
            highlightbackground='#2C2C2C',
            justify='center'
        )
        self.search_entry.pack(fill='both', expand='yes')

        ## botones busquedas
        self.div_search_button = Frame(self.div_search)
        self.div_search_button.config(
            bg=self.div_search_button.master['background']
        )
        self.div_search_button.pack(side='right', fill='both')

        self.bt_search = Button(self.div_search_button)
        self.bt_search.configure(
            border=0, borderwidth=0, width=10,
            background='#666666',
            foreground='#FFF',
            activebackground='#666666',
            activeforeground='#FFF',
            highlightbackground='#666666',
            text='Buscar'
        )
        self.bt_search.pack(side='left', padx=1, fill='both', expand='yes')

        self.bt_add = Button(self.div_search_button)
        self.bt_add.image = PhotoImage(data=b64decode(self.parser.get('tk', 'bt-plus')))
        self.bt_add.configure(
            border=0, borderwidth=0,
            image=self.bt_add.image,
            background=self.bt_add.master['background'],
            activebackground=self.bt_add.master['background'],
            highlightbackground=self.bt_add.master['background']
        )
        self.bt_add.pack(side='right', padx=5)

        self.bt_open = Button(self.div_search_button)
        self.bt_open.configure(
            border=0, borderwidth=0, width=10,
            background='#666666',
            foreground='#FFF',
            activebackground='#666666',
            activeforeground='#FFF',
            highlightbackground='#666666',
            text='AbirXLSX'
        )
        self.bt_open.pack(side='right', padx=1, fill='both', expand='yes')


        # resultados de busquedas
        self.div_results = Frame(self)
        self.div_results.configure(background='#FFF')
        self.div_results.pack(fill='both', expand='yes', padx=20, pady=10)


        ## resultados encontrados
        self.div_matches = Frame(self.div_results)
        self.div_matches.configure(background='#FFF')
        self.div_matches.pack(side='left', fill='both', expand='yes')

        self.matches_header = Label(self.div_matches)
        self.matches_header.configure(
            background='#2C2C2C',
            foreground='#FFF',
            text='Resultados Encontrados'
        )
        self.matches_header.pack(fill='both', ipady=2)

        self.matches_list = Listbox(self.div_matches)
        self.scroll_matches = Scrollbar(self.div_matches, orient='vertical')
        self.matches_list.configure(
            background='#FFF',
            foreground='#2C2C2C',
            selectbackground='#2C2C2C',
            selectforeground='#FFF',
            highlightbackground='#2C2C2C',
            selectmode='extended',
            yscrollcommand=self.scroll_matches.set
        )
        self.scroll_matches.config(command=self.matches_list.yview)
        self.scroll_matches.pack(side='right', fill='y')
        self.matches_list.pack(fill='both', expand='yes')


        ## resultados no encontrados
        self.div_notmatches = Frame(self.div_results)
        self.div_notmatches.configure(background='#FFF')
        self.div_notmatches.pack(side='right', fill='both', padx=5)

        self.notmatches_header = Label(self.div_notmatches)
        self.notmatches_header.configure(
            background='#2C2C2C',
            foreground='#FFF',
            text='No encontrados'
        )
        self.notmatches_header.pack(fill='both', ipady=2)

        self.notmatches_list = Listbox(self.div_notmatches)
        self.scroll_notmatches = Scrollbar(self.div_notmatches, orient='vertical')
        self.scroll_notmatches.pack(side='right', fill='y')
        self.notmatches_list.configure(
            background='#FFF',
            foreground='#2C2C2C',
            selectbackground='#2C2C2C',
            selectforeground='#FFF',
            highlightbackground='#2C2C2C',
            selectmode='extended',
            yscrollcommand=self.scroll_notmatches.set)
        self.scroll_notmatches.config(command=self.notmatches_list.yview)
        self.notmatches_list.pack(fill='both', expand='yes')


        # barra de sistema
        self.div_system = Frame(self)
        self.div_system.configure(background='#444444')
        self.div_system.pack(fill='both')

        self.status = Label(self.div_system)
        self.status.configure(background=self.status.master['background'],
                              foreground='#FFF')
        self.status.pack(fill='both')