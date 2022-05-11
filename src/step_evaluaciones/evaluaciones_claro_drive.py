import time

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from src.step_evaluaciones import constantes_evaluaciones_claro_drive as const_claro_drive
from src.utils.utils_evaluaciones import UtilsEvaluaciones
from src.utils.utils_format import FormatUtils
from src.utils.utils_html import ValidacionesHtml
from src.utils.utils_temporizador import Temporizador
from src.webdriver_actions.html_actions import HtmlActions


class EvaluacionesClaroDriveSteps:

    @staticmethod
    def ingreso_pagina_principal_claro_drive(webdriver: WebDriver, json_eval):
        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        try:
            url_claro_drive = FormatUtils.lector_archivo_ini().get('Driver', 'url_claro_drive')
            webdriver.get(url_claro_drive)

            # localiza boton de inicio en la pagina principal
            HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver, 15, id=const_claro_drive.INGRESO_PAGINA_PRINCIPAL_ID_INPUT_LOGIN)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 0, 0, True, const_claro_drive.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO. \
                format(e.msg)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO. \
                format(e.msg)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO. \
                format(e.msg)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        except InvalidArgumentException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO. \
                format(e.msg)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        except WebDriverException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO. \
                format(e.msg)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 0, tiempo_step_inicio, fecha_inicio)

        return json_eval

    @staticmethod
    def inicio_sesion_claro_drive(webdriver_test_ux: WebDriver, json_eval, argumentos_json):

        tiempo_step_inicio = None
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        # verifica que se haya iniciado sesion correctamente
        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_pagina_principal(json_eval):
            json_eval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecta(
                json_eval, tiempo_step_inicio, fecha_inicio, 1,
                const_claro_drive.MSG_OUTPUT_INICIO_SESION_MSG_ERROR_INGRESO_PAGINA_PRINCIPAL)

            return json_eval

        try:
            btn_inicio_sesion = HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, 6, id=const_claro_drive.INICIO_SESION_ID_INPUT_LOGIN)
            HtmlActions.click_html_element(btn_inicio_sesion, id=const_claro_drive.INICIO_SESION_ID_INPUT_LOGIN)

            input_email = HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, 6, class_name=const_claro_drive.INICIO_SESION_CLASS_NAME_INPUT_EMAIL)
            HtmlActions.enviar_data_keys(
                input_email, data_key=argumentos_json[const_claro_drive.JSON_ARG_USER],
                class_name=const_claro_drive.INICIO_SESION_CLASS_NAME_INPUT_EMAIL)

            btn_siguiente = HtmlActions.webdriver_wait_presence_of_element_located(webdriver_test_ux, 6, id='send')
            HtmlActions.click_html_element(btn_siguiente, id='send')

            input_password = HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, 6, class_name=const_claro_drive.INICIO_SESION_CLASS_NAME_INPUT_PASSWORD)
            input_password.send_keys(argumentos_json[const_claro_drive.JSON_ARG_PASSWORD])

            btn_siguiente = HtmlActions.webdriver_wait_presence_of_element_located(webdriver_test_ux, 6, id='send')
            HtmlActions.click_html_element(btn_siguiente, id='send')

            # inicia el tiempo de inicio
            tiempo_step_inicio = Temporizador.obtener_tiempo_timer()

            HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, 120, class_name=const_claro_drive.INICIO_SESION_CLASS_NAME_BTN_CREATE_RESOURCE)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 1, 0, True, const_claro_drive.MSG_OUTPUT_INICIO_SESION_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_INICIO_SESION_SIN_EXITO. \
                format(e.msg)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 1, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_INICIO_SESION_SIN_EXITO. \
                format(e.msg)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 1, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_INICIO_SESION_SIN_EXITO. \
                format(e.msg)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 1, 0, False, msg_output)

        except StaleElementReferenceException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_INICIO_SESION_SIN_EXITO. \
                format(e.msg)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 1, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 1, tiempo_step_inicio, fecha_inicio)

        return json_eval

    @staticmethod
    def carga_archivo_claro_drive(webdriver_test_ux: WebDriver, path_archivo_carga: str, json_eval):

        tiempo_step_inicio = None
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        # verifica que se haya iniciado sesion correctamente
        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_sesion(json_eval):
            json_eval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecta(
                json_eval, tiempo_step_inicio, fecha_inicio, 2,
                const_claro_drive.MSG_OUTPUT_CARGA_ARCHIVO_MSG_ERROR_INICIO_SESION)

            return json_eval

        try:
            HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, 10, class_name=const_claro_drive.CARGA_ARCHIVO_CLASS_NAME_BTN_CREATE_RESOURCE)

            HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, 180, class_name=const_claro_drive.CARGA_ARCHIVO_CLASS_NAME_FILE_NAME_READER)

            HtmlActions.webdriver_wait_presence_of_element_located(webdriver_test_ux, 60, class_name='Recent')

            HtmlActions.webdriver_wait_presence_of_element_located(webdriver_test_ux, 50, id='quota-wrapper')

            input_file = HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, 50, id=const_claro_drive.CARGA_ARCHIVO_ID_INPUT_FILE_START)

            HtmlActions.enviar_data_keys(
                input_file, path_archivo_carga, id=const_claro_drive.CARGA_ARCHIVO_ID_INPUT_FILE_START)

            #ValidacionesHtml.verificar_ventana_archivo_duplicado(webdriver_test_ux)

            tiempo_step_inicio = UtilsEvaluaciones.esperar_carga_total_de_archivo(
                webdriver_test_ux, tiempo_step_inicio)

            # print('tiempo step inicio afuera de la funcion: {}'.format(tiempo_step_inicio))

            HtmlActions.verificar_display_flex_modal_mensaje_de_exito(webdriver_test_ux)

            btn_cerrar_div_progreso_carga_archivo = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, 6, class_name=const_claro_drive.CARGA_ARCHIVO_CLASS_NAME_UP_CLOSE)

            HtmlActions.verificar_display_flex_modal_mensaje_de_exito(webdriver_test_ux)

            HtmlActions.click_html_element(
                btn_cerrar_div_progreso_carga_archivo, class_name=const_claro_drive.CARGA_ARCHIVO_CLASS_NAME_UP_CLOSE)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 2, 0, True, const_claro_drive.MSG_OUTPUT_CARGA_ARCHIVO_EXITOSO)

        except NoSuchElementException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_CARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 2, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_CARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 2, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_CARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 2, 0, False, msg_output)

        except StaleElementReferenceException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_CARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 2, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 2, tiempo_step_inicio, fecha_inicio)

        return json_eval

    @staticmethod
    def descarga_archivo_claro_drive(webdriver_test_ux: WebDriver, nombre_archivo_sin_ext: str, json_eval,
                                     ext_archivo: str):

        nombre_completo_de_la_imagen = '{}{}'.format(nombre_archivo_sin_ext, ext_archivo)
        tiempo_step_inicio = None
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        # verifica que se haya iniciado sesion correctamente
        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_sesion(json_eval):
            json_eval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecta(
                json_eval, tiempo_step_inicio, fecha_inicio, 3,
                const_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_MSG_ERROR_INICIO_SESION)

            return json_eval

        # verifica que se haya iniciado sesion correctamente
        if not UtilsEvaluaciones.se_cargo_correctamente_el_fichero(json_eval):
            json_eval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecta(
                json_eval, tiempo_step_inicio, fecha_inicio, 3,
                const_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_MSG_ERROR_CARGA_ARCHIVO)

            return json_eval

        try:
            # verifica que ya no se presente una modal de exito, para no interrumpir los clics en el portal
            HtmlActions.verificar_display_flex_modal_mensaje_de_exito(webdriver_test_ux)

            # busqueda del input o barra de busqueda
            input_busqueda = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, 20, id=const_claro_drive.DESCARGA_ARCHIVO_ID_SEARCH_BOX)

            # se ingresa cada caracter a la barra de busqueda con un lapso de tiempo
            for character in nombre_completo_de_la_imagen:
                HtmlActions.enviar_data_keys(
                    input_busqueda, character, id=const_claro_drive.DESCARGA_ARCHIVO_ID_SEARCH_BOX)
                time.sleep(.25)

            # se envia una tecla Enter, para que realice la busqueda del archivo
            HtmlActions.enviar_data_keys(
                input_busqueda, Keys.RETURN, id=const_claro_drive.DESCARGA_ARCHIVO_ID_SEARCH_BOX)

            # se establece un sleep de 5 segundos para que refresque la pantalla y muestre los
            # archivos localizados
            time.sleep(5)

            # localiza el archivo a descargar en el portal
            archivo_localizado_por_descargar = HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, 20, class_name='filename')

            # verifica que ya no se presente una modal de exito, para no interrumpir los clics en el portal
            HtmlActions.verificar_display_flex_modal_mensaje_de_exito(webdriver_test_ux)

            boton_sub_menu_actions = HtmlActions.webdriver_wait_presence_of_element_located(
                archivo_localizado_por_descargar, 20, class_name='open-menu')

            HtmlActions.click_html_element(boton_sub_menu_actions, class_name='open-menu')

            boton_descargar = HtmlActions.webdriver_wait_presence_of_element_located(
                boton_sub_menu_actions, 20, xpath='//li[@class="download action"]')

            HtmlActions.click_html_element(boton_descargar, xpath='//li[@class="download action"]')

            HtmlActions.verificar_display_flex_modal_mensaje_de_exito(webdriver_test_ux)

            tiempo_step_inicio = Temporizador.obtener_tiempo_timer()

            UtilsEvaluaciones.verificar_descarga_en_ejecucion(nombre_archivo_sin_ext, ext_archivo)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 3, 0, True, const_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_EXITOSO)

        except NoSuchElementException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        except StaleElementReferenceException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        except ElementNotInteractableException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 3, tiempo_step_inicio, fecha_inicio)

        return json_eval

    @staticmethod
    def borrar_archivo_claro_drive(webdriver_test_ux: WebDriver, json_eval, nombre_archivo_sin_ext: str,
                                   ext_archivo: str):

        nombre_completo_de_la_imagen = '{}{}'.format(nombre_archivo_sin_ext, ext_archivo)
        tiempo_step_inicio = None
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        # verifica que se haya iniciado sesion correctamente
        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_sesion(json_eval):
            json_eval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecta(
                json_eval, tiempo_step_inicio, fecha_inicio, 4,
                const_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_MSG_ERROR_INICIO_SESION)

            return json_eval

        # verifica que se haya iniciado sesion correctamente
        if not UtilsEvaluaciones.se_cargo_correctamente_el_fichero(json_eval):
            json_eval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecta(
                json_eval, tiempo_step_inicio, fecha_inicio, 4,
                const_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_MSG_ERROR_CARGA_ARCHIVO)

            return json_eval

        try:

            HtmlActions.verificar_display_flex_modal_mensaje_de_exito(webdriver_test_ux)

            # localiza el archivo a eliminar en el portal
            archivo_localizado_por_descargar = HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, 20, class_name='filename')

            # verifica que ya no se presente una modal de exito, para no interrumpir los clics en el portal
            HtmlActions.verificar_display_flex_modal_mensaje_de_exito(webdriver_test_ux)

            # se localiza el boton de sub menu del archivo a borrar
            boton_sub_menu_actions = HtmlActions.webdriver_wait_presence_of_element_located(
                archivo_localizado_por_descargar, 20, class_name='open-menu')

            # se realiza un clic en el boton del submenu
            HtmlActions.click_html_element(boton_sub_menu_actions, class_name='open-menu')

            # se busca el boton de eliminar, el cual contiene el submenu
            boton_eliminar = HtmlActions.webdriver_wait_presence_of_element_located(
                boton_sub_menu_actions, 20, xpath='//li[@class="delete action"]')

            # se verifica que no este presente la modal de algun mensaje, para que no
            # intervenga en el clic al boton de eliminar
            HtmlActions.verificar_display_flex_modal_mensaje_de_exito(webdriver_test_ux)

            # se realiza un clic al boton de eliminar
            HtmlActions.click_html_element(boton_eliminar, xpath='//li[@class="delete action"]')

            # se empieza a tomar el tiempo de duracion de la eliminacion del archivo
            tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
            UtilsEvaluaciones.esperar_aparicion_modal_de_exito(webdriver_test_ux)

            # se establecen los resultados exitosos en el json
            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 4, 0, True, const_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_EXITOSO)

        except NoSuchElementException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 4, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 4, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 4, 0, False, msg_output)

        except StaleElementReferenceException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 4, 0, False, msg_output)

        except ElementNotInteractableException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 4, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 4, tiempo_step_inicio, fecha_inicio)

        return json_eval

    @staticmethod
    def cerrar_sesion_claro_drive(webdriver_test_ux: WebDriver, json_eval):
        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        # verifica que se haya iniciado sesion correctamente
        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_sesion(json_eval):
            json_eval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecta(
                json_eval, tiempo_step_inicio, fecha_inicio, 5,
                const_claro_drive.MSG_OUTPUT_CIERRE_SESION_MSG_ERROR_INICIO_SESION)

            return json_eval

        try:
            boton_cerrar_sesion = HtmlActions.webdriver_wait_invisibility_of_element_located(
                webdriver_test_ux, 20, xpath=const_claro_drive.CERRAR_SESION_XPATH_LI_LOGOUT)

            link_cierre_de_sesion = boton_cerrar_sesion.get_attribute(const_claro_drive.CERRAR_SESION_ATTR_HREF)

            webdriver_test_ux.get(link_cierre_de_sesion)

            tiempo_step_inicio = Temporizador.obtener_tiempo_timer()

            HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, 20, id=const_claro_drive.CERRAR_SESION_ID_LOGIN)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 5, 0, True, const_claro_drive.MSG_OUTPUT_CIERRE_SESION_EXITOSO)

        except NoSuchElementException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_CIERRE_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 5, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_CIERRE_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 5, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_CIERRE_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 5, 0, False, msg_output)

        except ElementNotInteractableException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_CIERRE_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 5, 0, False, msg_output)

        except StaleElementReferenceException as e:
            msg_output = const_claro_drive.MSG_OUTPUT_CIERRE_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 5, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 5, tiempo_step_inicio, fecha_inicio)

        return json_eval
