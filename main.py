#!usr/bin/python3
#-*- coding: utf-8 -*-

from lib.mainwindow import MainWindow
from lib.utils import get_openfiles
from lib.utils import create_dataframe, delete_localfiles
from lib.utils import get_local_csvfiles
from lib.utils import get_values_from_string
from lib.utils import search_values_on_csv
from lib.utils import get_csv_headers
from lib.utils import delete_localfiles


class Main(MainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.local_dir = '.local'
        self.local_filenames = []
    

    def main_search(self):
        # obtener valores desde el input
        input_values = get_values_from_string(self.get_search_input())

        # obtener ruta del archivo elegido en la interfaz
        current_filename = self.get_currentfile()

        # busqueda principal de valores en dataset precargado
        try:
            matches, notmatches = search_values_on_csv(
                search_values=input_values,
                csv_dir=self.local_dir,
                csv_filename=current_filename
            )
        
        except IsADirectoryError:
            status_message = 'No hay archivos cargados para cotejar con los datos'
            self.set_status(message=status_message)
            return
        
        except FileNotFoundError:
            status_message = 'No hay archivos cargados para cotejar con los datos'
            self.set_status(message=status_message)
            return

        # actualizar mensaje del sistema
        status_message = 'Buscados:%s - Encontrados:%s - No encontrados:%s'
        status_message = status_message % (
            len(input_values),len(matches),len(notmatches)
        )
        self.set_status(message=status_message)


        # presentacion en interfaz de resultados encontrados
        csvHeaders = get_csv_headers(self.local_dir, current_filename)
        self.set_match_table_headers(csvHeaders)
        self.insert_match(*matches)

        # presentacion en interfaz de resultados no encontrados        
        self.insert_notmatch(*notmatches)


    def openfile(self):
        self.local_filenames = []

        # actualizar mensajes de sistema
        status_message = 'Cargar archivos Excel'
        self.set_status(message=status_message)

        filenames = get_openfiles()
        if len(filenames):
            progress_count = 0
            progress_step = 100 // len(filenames)

            for i in filenames:
                try:
                    local_filepath = create_dataframe(i, self.local_dir)
                except:
                    status_message = 'Ocurrio un error al cargar archivo'
                    self.set_status(message=status_message)

                else:
                    self.local_filenames.append(local_filepath)
                    filename = i.split('/')[-1]
                    status_message = 'Archivo cargado correctamente: %s' % filename
                    self.set_status(message=status_message)

                    # barra de progreso
                    self.ui_mainwindow.progressbar.show()
                    progress_count = progress_count + progress_step
                    self.ui_mainwindow.progressbar.setValue(progress_count)

        else:
            status_message = 'No se seleccionaron archivos para cargar'
            self.set_status(message=status_message)
            return
        
        self.ui_mainwindow.progressbar.hide() # ocultar barra de progreso

        status_message = 'Se cargaron correctamente %s archivos' % len(self.local_filenames)
        self.set_status(message=status_message)
        self.load_localfiles()
    

    def clear_localfiles(self):
        files = delete_localfiles(self.local_dir)
        status_message = 'Se han eliminado %s archivos' % len(files)
        self.set_status(message=status_message)
        self.load_localfiles()

        self.load_localfiles()


    def load_localfiles(self):
        # se busca en archivos locales para construir combobox
        local_files = get_local_csvfiles(self.local_dir)
        self.set_combobox_items(*local_files)



    def execute(self):
        self.ui_mainwindow.search_button.clicked.connect(self.main_search)
        self.ui_mainwindow.openfile_button.clicked.connect(self.openfile)
        self.ui_mainwindow.clear_button.clicked.connect(self.clear_localfiles)
        self.load_localfiles()
        
        self.q_mainwindow.show()


if __name__ == '__main__':
    import sys
    app = Main()
    app.execute()
    sys.exit(app.exec_())