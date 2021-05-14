from os import path
from pathlib import Path
from src.step_evaluaciones.evaluaciones_claro_drive import EvaluacionesClaroDriveSteps
from src.utils.utils_format import FormatUtils
from src.utils.utils_main import UtilsMain
from src.utils.utils_temporizador import Temporizador
from src.validaciones_json.json_evaluacion_base import GeneradorJsonBaseEvaluacion
from src.webdriver_config.config_webdriver import ConfiguracionWebDriver
from src.webdriver_config import config_constantes
import configparser
import json
import sys
import time
import src.validaciones_json.constantes_json as constantes_json


def verificacion_estatus_final(json_evaluacion):
    """

    :param json_evaluacion:
    :return:
    """
    val_paso_1 = True if json_evaluacion["steps"][0]["status"] == constantes_json.SUCCESS else False
    val_paso_2 = True if json_evaluacion["steps"][1]["status"] == constantes_json.SUCCESS else False
    val_paso_3 = True if json_evaluacion["steps"][2]["status"] == constantes_json.SUCCESS else False
    val_paso_4 = True if json_evaluacion["steps"][3]["status"] == constantes_json.SUCCESS else False
    val_paso_5 = True if json_evaluacion["steps"][4]["status"] == constantes_json.SUCCESS else False
    val_paso_6 = True if json_evaluacion["steps"][5]["status"] == constantes_json.SUCCESS else False

    eval_final = val_paso_1 and val_paso_2 and val_paso_3 and val_paso_4 and val_paso_5 and val_paso_6

    return constantes_json.SUCCESS if eval_final else constantes_json.FAILED


def verificacion_script_argumentos():
    """
    Verifica que dentro de la ejecucion del script se haya establecido el parametro principal en formato JSON. De ser
    asi la funcion retornara True, en caso contrario retorna False

    :return:
    """
    validacion_completa = True

    argumentos_script = sys.argv[1:]

    if len(argumentos_script) == 0:
        print('No se encontraron parametros en la llamada del Script. Favor de establecer el parametro principal en'
              'formato JSON para la ejecucion correcta del Script.')
        validacion_completa = False

    return validacion_completa


def verificacion_script_argumento_json(argumento_script_json):
    """

    :param argumento_script_json:
    :return:
    """
    if not FormatUtils.cadena_a_json_valido(argumento_script_json):
        return False

    json_argumento_formateado = json.loads(argumento_script_json)

    if not FormatUtils.verificar_keys_json(json_argumento_formateado):
        return False

    elif not path.exists(json_argumento_formateado['pathImage']):
        print('La imagen/archivo por cargar dentro de la plataforma Claro Drive no fue localizado dentro del server, '
              'favor de verificar nuevamente el path de la imagen/archivo.')
        return False

    elif not path.isfile(json_argumento_formateado['pathImage']):
        print('El path de la imagen/archivo establecida, no corresponde a un archivo o imagen valida, favor de '
              'verificar nuevamente el path del archivo.')
        return False

    return True


def verificacion_archivo_config(archivo_config: configparser.ConfigParser):
    """
    Funcion el cual permite verificar que el archivo config.ini contenga todos los parametros necesarios. En caso
    de que contenga las secciones y keys establecidos, la funcion devolvera True, en caso contrario regresara False

    :return:
    """
    validacion_total = True

    bool_ruta = archivo_config.has_option('Driver', 'ruta')
    bool_web_driver = archivo_config.has_option('Driver', 'driverPorUtilizar')
    bool_folder_descargas = archivo_config.has_option('Driver', 'folder_descargas')
    bool_headless = archivo_config.has_option('Driver', 'headless')
    bool_url_claro_drive = archivo_config.has_option('Driver', 'url_claro_drive')

    if not bool_ruta:
        print('Favor de establecer el path del webdriver a utilizar dentro del archivo config.ini')
        validacion_total = False
    elif not bool_web_driver:
        print('Favor de establecer el tipo/nombre del webdriver a utilizar dentro del archivo config.ini')
        validacion_total = False
    elif not bool_folder_descargas:
        print('Favor de establecer el path en donde residiran las descargas dentro del archivo config.ini')
        validacion_total = False
    elif not bool_headless:
        print('Favor de establecer la opcion/configuracion headless dentro del archivo config.ini')
        validacion_total = False
    elif not bool_url_claro_drive:
        print('Favor de establecer la opcion/configuracion url_claro_drive dentro del archivo config.ini')
        validacion_total = False

    return validacion_total


def ejecucion_validaciones_claro_drive(webdriver, argumento_script_json):
    """

    :param webdriver:
    :param argumento_script_json:
    :return:
    """
    nombre_de_imagen_sin_extension = Path(argumento_script_json['pathImage']).stem
    nombre_de_imagen_con_extension = path.basename(argumento_script_json['pathImage'])
    config_constantes.NOMBRE_IMAGEN_POR_CARGAR_CON_EXTENSION = path.basename(argumento_script_json['pathImage'])
    extension_de_la_imagen = path.splitext(nombre_de_imagen_con_extension)[1]

    # establece los datetime de inicio para la prueba UX
    tiempo_inicial_ejecucion_prueba = Temporizador.obtener_tiempo_timer()
    fecha_prueba_inicial = Temporizador.obtener_fecha_tiempo_actual()

    # se genera el json de evaluacion
    json_evaluacion_claro_drive = GeneradorJsonBaseEvaluacion.generar_nuevo_template_json()

    json_evaluacion_claro_drive = EvaluacionesClaroDriveSteps.ingreso_pagina_principal_claro_drive(
        webdriver, json_evaluacion_claro_drive)

    json_evaluacion_claro_drive = EvaluacionesClaroDriveSteps.inicio_sesion_claro_drive(
        webdriver, json_evaluacion_claro_drive, argumento_script_json)

    json_evaluacion_claro_drive = EvaluacionesClaroDriveSteps.carga_archivo_claro_drive(
        webdriver, argumento_script_json['pathImage'], json_evaluacion_claro_drive)

    json_evaluacion_claro_drive = EvaluacionesClaroDriveSteps.descarga_archivo_claro_drive(
        webdriver, nombre_de_imagen_sin_extension, json_evaluacion_claro_drive, extension_de_la_imagen)

    json_evaluacion_claro_drive = EvaluacionesClaroDriveSteps.borrar_archivo_claro_drive(
        webdriver, json_evaluacion_claro_drive, nombre_de_imagen_sin_extension, extension_de_la_imagen)

    json_evaluacion_claro_drive = EvaluacionesClaroDriveSteps.cerrar_sesion_claro_drive(
        webdriver, json_evaluacion_claro_drive)

    tiempo_final_ejecucion_prueba = Temporizador.obtener_tiempo_timer() - tiempo_inicial_ejecucion_prueba
    fecha_prueba_final = Temporizador.obtener_fecha_tiempo_actual()

    json_evaluacion_claro_drive['start'] = fecha_prueba_inicial
    json_evaluacion_claro_drive['end'] = fecha_prueba_final
    json_evaluacion_claro_drive['time'] = tiempo_final_ejecucion_prueba
    json_evaluacion_claro_drive['status'] = verificacion_estatus_final(json_evaluacion_claro_drive)

    json_padre = {}
    json_padre.update({'body': json_evaluacion_claro_drive})

    time.sleep(2)

    webdriver.close()
    webdriver.quit()

    return json_padre


def main():
    """

    """
    # verificacion del archivo de configuracion (config.ini)
    archivo_config = FormatUtils.lector_archivo_ini()

    if not verificacion_archivo_config(archivo_config):
        sys.exit()

    param_archivo_config_path_web_driver = archivo_config.get('Driver', 'ruta')
    param_archivo_config_web_driver_por_usar = archivo_config.get('Driver', 'driverPorUtilizar')
    param_archivo_config_directorio_descargas = archivo_config.get('Driver', 'folder_descargas')

    # verificacion de argumentos dentro de la ejecucion del script
    if not verificacion_script_argumentos():
        sys.exit()

    argumentos_script = sys.argv[1:]
    argumento_script_json = argumentos_script[0]

    # verifica el formato del argumento JSON y obtiene cada uno de los parametros
    if not verificacion_script_argumento_json(argumento_script_json):
        sys.exit()

    argumento_script_json = json.loads(argumento_script_json)

    # establece la carpeta de descarga dinamica (donde se descargara la imagen desde el portal de claro drive)
    config_constantes.PATH_CARPETA_DESCARGA = UtilsMain.generar_carpeta_descarga_dinamica(
        argumento_script_json['pathImage'])

    UtilsMain.crear_directorio(config_constantes.PATH_CARPETA_DESCARGA)

    # se establece la configuracion del webdriver
    webdriver_config = ConfiguracionWebDriver(param_archivo_config_path_web_driver,
                                              param_archivo_config_web_driver_por_usar,
                                              param_archivo_config_directorio_descargas)

    # se establece y obtiene el webdriver/navegar para la ejecucion de las pruebas UX en claro drive
    webdriver_ux_test = webdriver_config.configurar_obtencion_web_driver()

    # webdriver_ux_test.set_window_position(0, 0)
    # webdriver_ux_test.set_window_size(1366, 768)

    # inicia depuracion de descargas antiguas
    UtilsMain.depurar_carpeta_de_descargas(param_archivo_config_directorio_descargas)

    resultado_json_evaluacines_ux_claro_drive = ejecucion_validaciones_claro_drive(webdriver_ux_test,
                                                                                   argumento_script_json)

    UtilsMain.eliminar_directorio_con_contenido(config_constantes.PATH_CARPETA_DESCARGA)

    print(json.dumps(resultado_json_evaluacines_ux_claro_drive))


main()
