from os import listdir, mkdir, umask, rename
from os.path import isdir, isfile, join, getmtime
from src.utils.utils_format import FormatUtils
from pathlib import Path
import shutil
import datetime
import random
import string


class UtilsMain:

    @staticmethod
    def verificar_path_es_directorio(path_por_analizar):
        return isdir(path_por_analizar)

    @staticmethod
    def obtener_lista_ficheros_en_directorio(path_directorio):
        lista_ficheros = listdir(path_directorio)
        lista_archivos = []

        # return [archivo for archivo in listdir(path_directorio) if isfile(join(path_directorio, archivo))]
        for archivo in lista_ficheros:
            try:
                if isfile(join(path_directorio, archivo)):
                    lista_archivos.append(archivo)
            except PermissionError:
                pass

        return lista_archivos

    @staticmethod
    def obtener_lista_folders_en_directorio(path_directorio):
        lista_ficheros = listdir(path_directorio)
        lista_folders = []

        # return [archivo for archivo in listdir(path_directorio) if isfile(join(path_directorio, archivo))]
        for archivo in lista_ficheros:
            try:
                if isdir(join(path_directorio, archivo)):
                    lista_folders.append(archivo)
            except PermissionError:
                pass

        return lista_folders

    @staticmethod
    def generar_cadena_alafanumerica_aleatoria(longitud_cadena):
        letras_y_numeros = string.ascii_letters + string.digits
        cadena = ''.join((random.choice(letras_y_numeros) for i in range(longitud_cadena)))
        return cadena

    @staticmethod
    def generar_carpeta_descarga_dinamica(path_imagen_prueba_claro_drive):
        path_descarga_hija = '{}_{}_{}'
        archivo_config_ini = FormatUtils.lector_archivo_ini()
        path_descarga_raiz = archivo_config_ini.get('Driver', 'folder_descargas')
        nombre_archivo_sin_extension = Path(path_imagen_prueba_claro_drive).stem
        datetime_fecha_actual = datetime.datetime.today()
        cadena_fecha_hora_actual = '{}_{}_{}_{}_{}_{}'.format(
            datetime_fecha_actual.day, datetime_fecha_actual.month, datetime_fecha_actual.year,
            datetime_fecha_actual.hour, datetime_fecha_actual.minute, datetime_fecha_actual.second)

        path_descarga_hija = path_descarga_hija.format(nombre_archivo_sin_extension, cadena_fecha_hora_actual,
                                                       UtilsMain.generar_cadena_alafanumerica_aleatoria(6))

        path_descarga_hija = join(path_descarga_raiz, path_descarga_hija)

        return path_descarga_hija

    @staticmethod
    def crear_directorio(path_directorio_por_crear):
        try:
            umask(0)
            mkdir(path_directorio_por_crear)
            rename(path_directorio_por_crear, path_directorio_por_crear)
        except NotADirectoryError as e:
            print('Sucedio un error al intentar crear el directorio {}: {}'.format(path_directorio_por_crear, e))
        except IsADirectoryError as e:
            print('Sucedio un error al intentar crear el directorio {}: {}'.format(path_directorio_por_crear, e))
        except OSError as e:
            print('Sucedio un error al intentar crear el directorio {}: {}'.format(path_directorio_por_crear, e))

    @staticmethod
    def eliminar_directorio_con_contenido(path_directorio_por_borrar):
        shutil.rmtree(path=path_directorio_por_borrar, ignore_errors=True)

    @staticmethod
    def depurar_carpeta_de_descargas(path_carpeta_descargas: str, segundos_a_verificar: int = 7200):

        lista_carpetas_por_eliminar = UtilsMain.obtener_lista_folders_en_directorio(path_carpeta_descargas)
        fecha_actual = datetime.datetime.now()

        for directorio in lista_carpetas_por_eliminar:
            abs_path_directorio = join(path_carpeta_descargas, directorio)
            date_timestap = getmtime(abs_path_directorio)
            fecha_archivo = datetime.datetime.fromtimestamp(date_timestap)
            diferencia_segundos = (fecha_actual - fecha_archivo).seconds

            if diferencia_segundos > segundos_a_verificar:
                UtilsMain.eliminar_directorio_con_contenido(abs_path_directorio)
