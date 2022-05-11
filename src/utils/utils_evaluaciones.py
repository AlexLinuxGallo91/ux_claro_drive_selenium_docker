from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webdriver import WebDriver

import src.validaciones_json.constantes_json as contantes_json
from src.utils.utils_format import FormatUtils
from src.utils.utils_main import UtilsMain
from src.utils.utils_temporizador import Temporizador
from src.webdriver_actions.html_actions import HtmlActions
from src.webdriver_config import config_constantes
import time


class UtilsEvaluaciones:

    @staticmethod
    def finalizar_tiempos_en_step(json_eval, indice: int, tiempo_step_inicio, fecha_inicio):

        if tiempo_step_inicio is None:
            tiempo_step_inicio = Temporizador.obtener_tiempo_timer()

        tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
        fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
        json_eval["steps"][indice]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
        json_eval["steps"][indice]["start"] = fecha_inicio
        json_eval["steps"][indice]["end"] = fecha_fin

        return json_eval

    @staticmethod
    def establecer_output_status_step(json_eval, indice: int, sub_indice: int, paso_exitoso: bool, mensaje_output: str):

        status_del_step = contantes_json.SUCCESS if paso_exitoso else contantes_json.FAILED

        json_eval["steps"][indice]["output"][sub_indice]["status"] = status_del_step
        json_eval["steps"][indice]["status"] = status_del_step
        json_eval["steps"][indice]["output"][sub_indice]["output"] = mensaje_output

        return json_eval

    @staticmethod
    def generar_json_inicio_de_sesion_incorrecta(json_eval, tiempo_step_inicio, fecha_inicio, indice: int,
                                                 msg_output: str):

        if tiempo_step_inicio is None:
            tiempo_step_inicio = Temporizador.obtener_tiempo_timer()

        json_eval["steps"][indice]["output"][0]["status"] = contantes_json.FAILED
        json_eval["steps"][indice]["status"] = contantes_json.FAILED
        json_eval["steps"][indice]["output"][0]["output"] = msg_output

        tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
        fecha_fin = Temporizador.obtener_fecha_tiempo_actual()

        json_eval["steps"][indice]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
        json_eval["steps"][indice]["start"] = fecha_inicio
        json_eval["steps"][indice]["end"] = fecha_fin

        return json_eval

    @staticmethod
    def se_ingreso_correctamente_a_la_sesion(json_eval):
        return True if json_eval["steps"][1]["status"] == contantes_json.SUCCESS else False

    @staticmethod
    def se_ingreso_correctamente_a_la_pagina_principal(json_eval):
        return True if json_eval["steps"][0]["status"] == contantes_json.SUCCESS else False

    @staticmethod
    def se_cargo_correctamente_el_fichero(json_eval):
        return True if json_eval["steps"][2]["status"] == contantes_json.SUCCESS else False

    @staticmethod
    def verificar_descarga_en_ejecucion(nombre_del_archivo, extension_del_archivo):
        tiempo_inicio = Temporizador.obtener_tiempo_timer()
        se_descargo_el_archivo_exitosamente = False
        archivo_a_localizar = '{}{}'.format(nombre_del_archivo, extension_del_archivo)

        while (Temporizador.obtener_tiempo_timer() - tiempo_inicio) < 180:
            try:
                lista_archivos = UtilsMain.obtener_lista_ficheros_en_directorio(config_constantes.PATH_CARPETA_DESCARGA)

                if archivo_a_localizar in lista_archivos:
                    se_descargo_el_archivo_exitosamente = True
                    break
            except PermissionError:
                continue

        if not se_descargo_el_archivo_exitosamente:
            raise TimeoutException(msg='Han transcurrido 3 minutos sin finalizar la descarga del archivo {} desde '
                                       'el portal Claro Drive'.format(archivo_a_localizar))

    @staticmethod
    def esperar_aparicion_modal_de_exito(webdriver: WebDriver, tiempo_de_espera: int = 10):

        tiempo_de_inicio = Temporizador.obtener_tiempo_timer()
        tiempo_transcurrido = 0

        while tiempo_transcurrido < tiempo_de_espera:
            tiempo_transcurrido = Temporizador.obtener_tiempo_timer() - tiempo_de_inicio
            modal_de_exito = webdriver.find_elements_by_xpath('//div[@class="row type-success"]')

            if len(modal_de_exito) == 1:

                modal = modal_de_exito[0]

                if modal.is_displayed() and modal.is_enabled():
                    break

    @staticmethod
    def esperar_desaparicion_modal_exito(webdriver: WebDriver, tiempo_de_espera: int = 10):
        tiempo_de_inicio = Temporizador.obtener_tiempo_timer()
        tiempo_transcurrido = 0

        while tiempo_transcurrido < tiempo_de_espera:
            tiempo_transcurrido = Temporizador.obtener_tiempo_timer() - tiempo_de_inicio
            modal_de_exito = webdriver.find_elements_by_xpath('//div[@class="row type-success"]')

            if len(modal_de_exito) == 0:
                break

    @staticmethod
    def esperar_carga_total_de_archivo(webdriver: WebDriver, tiempo_step_inicio, tiempo_de_espera: int = 720):
        tiempo_inicial_ejecucion_de_funcion = Temporizador.obtener_tiempo_timer()
        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        tiempo_transcurrido = 0
        se_cargo_correctamente_el_fichero = False
        mensaje_exception = 'Han transcurrido mas de 12 minutos, sin cargar correctamente el archivo dentro del ' \
                            'portal de Claro Drive'
        numero_de_cancelaciones_de_descargas = 0

        while tiempo_transcurrido < tiempo_de_espera:
            # en cada iteracion espera al menos un segundo
            time.sleep(1)
            tiempo_transcurrido = Temporizador.obtener_tiempo_timer() - tiempo_inicial_ejecucion_de_funcion
            modal_de_exito = webdriver.find_elements_by_xpath('//div[@class="up-file-actions isDone"]')
            modal_archivo_duplicado = webdriver.find_elements_by_class_name('oc-dialog')

            if len(modal_de_exito) == 1:
                se_cargo_correctamente_el_fichero = True
                break
            elif len(modal_archivo_duplicado) > 0:
                try:
                    modal_archivo_duplicado = webdriver.find_element_by_class_name('oc-dialog')

                    check_box_all_files = HtmlActions.webdriver_wait_presence_of_element_located(
                        modal_archivo_duplicado, 5,
                        xpath='//label[@for="checkbox-allnewfiles"][text()="Archivos Nuevos"]')

                    HtmlActions.click_html_element(
                        check_box_all_files, xpath='//label[@for="checkbox-allnewfiles"][text()="Archivos Nuevos"]')

                    boton_continuar = HtmlActions.webdriver_wait_element_to_be_clickable(
                        modal_archivo_duplicado, class_name='continue')

                    HtmlActions.click_html_element(boton_continuar, class_name='continue')

                    HtmlActions.webdriver_wait_until_not_presence_of_element_located(webdriver, class_name='oc-dialog')
                    continue
                except ElementNotInteractableException:
                    continue
                except NoSuchElementException:
                    continue
                except TimeoutException:
                    continue
                except ElementClickInterceptedException:
                    continue

            # print('entrando al header')
            header = webdriver.find_elements_by_class_name('up-header')

            if len(header) > 0:
                mensaje_de_carga = header[0]
                mensaje_de_carga = mensaje_de_carga.find_elements_by_tag_name('span')

                if len(mensaje_de_carga) > 0:
                    mensaje_de_carga = mensaje_de_carga[0]

                    if 'Se ha cancelado la carga' in mensaje_de_carga.text \
                            or '1 Subida en pausa' in mensaje_de_carga.text:

                        numero_de_cancelaciones_de_descargas = numero_de_cancelaciones_de_descargas + 1
                        # print('numero de cancelaciones: {}'.format(numero_de_cancelaciones_de_descargas))
                        #
                        # print('se procede a dar clic en el boton de reupload')

                        try:

                            boton_reupload = HtmlActions.webdriver_wait_element_to_be_clickable(
                                webdriver, class_name='ResumeUploadOption')

                            HtmlActions.click_html_element(boton_reupload, class_name='ResumeUploadOption')
                            # print('se dio click')
                            tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
                            time.sleep(1)

                            continue
                        except ElementNotInteractableException:
                            continue
                        except NoSuchElementException:
                            continue
                        except TimeoutException:
                            continue
                        except ElementClickInterceptedException:
                            continue

                    if numero_de_cancelaciones_de_descargas > 10:
                        se_cargo_correctamente_el_fichero = False
                        mensaje_exception = 'Ha sucedido un error durante la carga del archivo, se presenta el ' \
                                            'siguiente mensaje: {}'.format(mensaje_de_carga.text)
                        # # DEBUG
                        # path_debug_img = '/home/trjlha/scripts/ux/clarodrive/debug_screenshots/debug.png'
                        # webdriver.save_screenshot(path_debug_img)
                        break

        if se_cargo_correctamente_el_fichero:
            UtilsEvaluaciones.esperar_desaparicion_modal_exito(webdriver)
        else:
            raise TimeoutException(msg=mensaje_exception)

        # print('tiempo step inicio dentro de la funcion: {}'.format(tiempo_step_inicio))
        return tiempo_step_inicio
