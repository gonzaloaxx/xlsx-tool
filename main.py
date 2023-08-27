#!usr/bin/python3
#-*- coding: utf-8 -*-


from lib.tkapplication import TkApplication
from lib.tkpopups import get_openfilenames
from lib.tkpopups import askme_loadfiles
from lib.coreutils import create_dataframe
from lib.coreutils import get_values_from_string
from lib.coreutils import search_values_in_csv



class Main:
    def __init__(self) -> None:
        self.tkapplication = TkApplication()


    def openfiles(self, event=None):
        # actualizar mensajes de sistema
        message = 'Cargar archivos Excel'
        self.tkapplication.status['text'] = message
        self.tkapplication.status['background'] = '#444444'

        filenames = get_openfilenames()
        if len(filenames) and askme_loadfiles():
            try:
                count = create_dataframe(filenames)
            except:
                message = 'Ocurrio un error al cargar los archivos'
                self.tkapplication.status['text'] = message
                self.tkapplication.status['background'] = '#f25252'
            else:
                message = 'Se cargaron correctamente %s archivos' % count
                self.tkapplication.status['text'] = message
                self.tkapplication.status['background'] = '#444444'
        else:
            message = 'Error en la carga de archivos'
            self.tkapplication.status['text'] = message
            self.tkapplication.status['background'] = '#f25252'



    def search(self, event=None):
        # obtener valores del cuadro de busqueda
        search_string = self.tkapplication.search_entry.get()
        search_values = get_values_from_string(search_string)

        # busqueda principal de valores en dataset precargado
        try:
            matches, not_matches = search_values_in_csv(search_values)
        except FileNotFoundError:
            message = 'No hay archivos cargados para cotejar con los datos'
            self.tkapplication.status['text'] = message
            self.tkapplication.status['background'] = '#f25252'
            return

        # actualizar mensaje del sistema
        message = 'Buscados:%s - Encontrados:%s - No encontrados:%s'
        message = message % (len(search_values),len(matches),len(not_matches))
        
        self.tkapplication.status['text'] = message
        self.tkapplication.status['background'] = '#444444'

        # presentacion en interfaz de resultados encontrados
        self.tkapplication.insert_matches(*matches)
        # presentacion en interfaz de resultados no encontrados        
        self.tkapplication.insert_notmatches(*not_matches)



    def builder(self):
        self.tkapplication.bt_open['command'] = self.openfiles
        self.tkapplication.bt_search['command'] = self.search
        self.tkapplication.mainloop()

if __name__ == '__main__':
    app = Main()
    app.builder()