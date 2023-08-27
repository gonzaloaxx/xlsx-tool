#!usr/bin/python3
#-*- coding: utf-8 -*-

from lib.mainwindow import MainWindow
from lib.tkpreview import TkPreview


class TkApplication(MainWindow):
    def __init__(self):
        super().__init__()

        self.bind('<Control-q>', lambda x: self.destroy())
        self.bind('<Control-f>', self.focus_on_searchbar)
        self.search_entry.bind('<Control-v>', self.paste_event)
        self.search_entry.bind('<Return>', lambda x: self.bt_search.invoke())
        self.matches_list.bind('<Double-1>', self.show_match_preview)
        self.matches_list.bind('<Return>', self.show_match_preview)
        self.matches_list.bind('<Control-a>', self.select_all_matches)



    def focus_on_searchbar(self, event=None):
        self.search_entry.focus()
        self.search_entry.select_range(0, 'end')



    def select_all_matches(self, event=None):
        self.matches_list.select_set(0, 'end')



    def paste_event(self, event=None):
        self.search_entry.delete(0, 'end')


    def insert_matches(self, *args):
        self.matches_list.delete(0, 'end')
        
        for i in args:
            parser = [value.strip('{}') for value in i]
            self.matches_list.insert('end', '; '.join(parser))
        
        self.matches_list.focus()



    def insert_notmatches(self, *args):
        self.notmatches_list.delete(0, 'end')
        for i in args:
            self.notmatches_list.insert('end', i)



    def show_match_preview(self, event=None):
        try: selection = self.matches_list.selection_get()
        except: return
        else:
            self.toplevel = TkPreview(self)

            for i in selection.split('; '):
                self.toplevel.insert_reg(i)
            
            self.toplevel.preview.focus()
            self.toplevel.preview.selection_set(0,0)