from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.utils.utils_temporizador import Temporizador
from src.utils.utils_format import FormatUtils
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from src.utils.utils_html import ValidacionesHtml
from selenium.webdriver.common.keys import Keys
from src.utils.utils_evaluaciones import UtilsEvaluaciones
import src.validaciones_json.constantes_json as jsonConst


class EvaluacionesClaroDriveSteps:

    def ingreso_pagina_principal_claro_drive(self, webdriver: WebDriver, jsonEval):
        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        try:
            webdriver.get('https://www.clarodrive.com/')

            #localiza boton de inicio
            WebDriverWait(webdriver, 15).until(EC.presence_of_element_located((By.ID, 'login')))

            jsonEval["steps"][0]["output"][0]["status"] = jsonConst.SUCCESS
            jsonEval["steps"][0]["status"] = jsonConst.SUCCESS
            jsonEval["steps"][0]["output"][0]["output"] = 'Se ingresa correctamente a la pagina principal de Claro ' \
                                                          'Drive'

        except ElementNotInteractableException as e:
            jsonEval["steps"][0]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][0]["output"][0]["output"] = 'fue imposible ingresar principal de Claro Drive'

        except NoSuchElementException as e:
            jsonEval["steps"][0]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][0]["output"][0]["output"] = 'fue imposible ingresar principal de Claro Drive'
        except TimeoutException as e:
            jsonEval["steps"][0]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][0]["output"][0]["output"] = 'fue imposible ingresar principal de Claro Drive'

        tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
        fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
        jsonEval["steps"][0]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
        jsonEval["steps"][0]["start"] = fecha_inicio
        jsonEval["steps"][0]["end"] = fecha_fin

        return jsonEval

    def inicio_sesion_claro_drive(self, webdriver_test_ux: WebDriver, jsonEval, jsonArgs):

        tiempo_step_inicio = None
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        try:
            btn_inicio_sesion = WebDriverWait(webdriver_test_ux, 6).until(
                EC.presence_of_element_located((By.ID, 'login')))
            btn_inicio_sesion.click()

            input_email = WebDriverWait(webdriver_test_ux, 6).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'InputEmail')))
            input_email.send_keys(jsonArgs['user'])

            input_password = WebDriverWait(webdriver_test_ux, 6).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'InputPassword')))
            input_password.send_keys(jsonArgs['password'])

            btn_ingreso_cuenta = WebDriverWait(webdriver_test_ux, 6).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="INICIAR SESI\u00D3N"]')))
            btn_ingreso_cuenta.click()

            # inicia el tiempo de inicio
            tiempo_step_inicio = Temporizador.obtener_tiempo_timer()

            WebDriverWait(webdriver_test_ux, 120).until(EC.element_to_be_clickable(
                (By.CLASS_NAME, 'button-create-resource')))

            jsonEval["steps"][1]["output"][0]["status"] = jsonConst.SUCCESS
            jsonEval["steps"][1]["status"] = jsonConst.SUCCESS
            jsonEval["steps"][1]["output"][0]["output"] = 'Se ingresa correctamente al portal Claro Drive'

        except ElementNotInteractableException as e:
            jsonEval["steps"][1]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][1]["status"] = jsonConst.FAILED
            jsonEval["steps"][1]["output"][0]["output"] = 'fue imposible ingresar al portal Claro Drive'
        except NoSuchElementException as e:
            jsonEval["steps"][1]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][1]["status"] = jsonConst.FAILED
            jsonEval["steps"][1]["output"][0]["output"] = 'fue imposible ingresar al portal Claro Drive'
        except TimeoutException as e:
            jsonEval["steps"][1]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][1]["status"] = jsonConst.FAILED
            jsonEval["steps"][1]["output"][0]["output"] = 'fue imposible ingresar al portal Claro Drive'

        if tiempo_step_inicio is None:
            tiempo_step_inicio = Temporizador.obtener_tiempo_timer()

        tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
        fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
        jsonEval["steps"][1]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
        jsonEval["steps"][1]["start"] = fecha_inicio
        jsonEval["steps"][1]["end"] = fecha_fin

        return jsonEval

    def carga_archivo_claro_drive(self, webdriver_test_ux: WebDriver, path_archivo_carga: str, nombre_archivo_sin_ext: str,
                                  jsonEval):

        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        # verifica que se haya iniciado sesion correctamente
        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_sesion(jsonEval):
            jsonEval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecto(jsonEval, tiempo_step_inicio,
                fecha_inicio, 1, 'No fue posible realizar la carga del archivo. No se ingreso a la sesion de Claro '
                                 'Drive correctamente')
            return jsonEval

        try:
            boton_crear = WebDriverWait(webdriver_test_ux, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'button-create-resource')))

            boton_crear.click()

            WebDriverWait(webdriver_test_ux, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'file-name-header')))

            input_file = WebDriverWait(webdriver_test_ux, 20).until(
                EC.presence_of_element_located((By.ID, 'file_upload_start')))

            input_file.send_keys(path_archivo_carga)

            ValidacionesHtml.verificar_ventana_archivo_duplicado(webdriver_test_ux)

            WebDriverWait(webdriver_test_ux, 720).until(EC.presence_of_element_located(
                (By.XPATH, '//div[@class="up-file-actions isDone"]')))

            jsonEval["steps"][2]["output"][0]["status"] = jsonConst.SUCCESS
            jsonEval["steps"][2]["status"] = jsonConst.SUCCESS
            jsonEval["steps"][2]["output"][0]["output"] = 'Se realiza correctamente la carga del archivo'

        except NoSuchElementException:
            jsonEval["steps"][2]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][2]["status"] = jsonConst.FAILED
            jsonEval["steps"][2]["output"][0]["output"] = 'No fue posible realizar la carga del archivo'

        except ElementClickInterceptedException:
            jsonEval["steps"][2]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][2]["status"] = jsonConst.FAILED
            jsonEval["steps"][2]["output"][0]["output"] = 'No fue posible realizar la carga del archivo'

        except TimeoutException:
            jsonEval["steps"][2]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][2]["status"] = jsonConst.FAILED
            jsonEval["steps"][2]["output"][0]["output"] = 'No fue posible realizar la carga del archivo'

        tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
        fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
        jsonEval["steps"][2]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
        jsonEval["steps"][2]["start"] = fecha_inicio
        jsonEval["steps"][2]["end"] = fecha_fin

        return jsonEval

    def descarga_archivo_claro_drive(self, webdriver_test_ux: WebDriver, nombre_archivo_sin_ext: str, jsonEval,
                                     ext_archivo: str):

        nombre_completo_de_la_imagen = '{}{}'.format(nombre_archivo_sin_ext, ext_archivo)
        tiempo_step_inicio = 0
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        # verifica que se haya iniciado sesion correctamente
        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_sesion(jsonEval):
            jsonEval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecto(jsonEval, tiempo_step_inicio,
                fecha_inicio, 2,'No fue posible realizar la descarga del archivo. No se ingreso a la sesion de Claro '
                'Drive correctamente')

            return jsonEval

        try:
            webdriver_test_ux.refresh()

            input_busqueda = WebDriverWait(webdriver_test_ux, 20).until(
                EC.element_to_be_clickable((By.ID, 'searchbox')))

            input_busqueda.click()
            input_busqueda.send_keys(nombre_completo_de_la_imagen)
            input_busqueda.send_keys(Keys.RETURN)

            WebDriverWait(webdriver_test_ux, 20).until(EC.visibility_of_element_located((By.CLASS_NAME,'result')))

            archivo_a_descargar = WebDriverWait(webdriver_test_ux, 20).until(
                EC.element_to_be_clickable((By.XPATH,
                '//span[@class="name-without-extension"][text()="{} "]'.format(nombre_archivo_sin_ext))))

            archivo_a_descargar.click()

            btn_descarga = WebDriverWait(webdriver_test_ux, 20).until(EC.element_to_be_clickable(
                (By.XPATH, '//input[@type="button"][@class="menuItem svg downloadImage icon-download icon-32"]')))

            btn_descarga.click()
            tiempo_step_inicio = Temporizador.obtener_tiempo_timer()

            UtilsEvaluaciones.verificar_descarga_en_ejecucion(nombre_archivo_sin_ext, ext_archivo)

            jsonEval["steps"][3]["output"][0]["status"] = jsonConst.SUCCESS
            jsonEval["steps"][3]["status"] = jsonConst.SUCCESS
            jsonEval["steps"][3]["output"][0]["output"] = 'Se realiza la descarga del archivo correctamente'
        except NoSuchElementException as e:
            jsonEval["steps"][3]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][3]["status"] = jsonConst.FAILED
            jsonEval["steps"][3]["output"][0][
                "output"] = 'No fue posible realizar la descarga del archivo correctamente: {}'.format(e)
        except ElementClickInterceptedException as e:
            jsonEval["steps"][3]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][3]["status"] = jsonConst.FAILED
            jsonEval["steps"][3]["output"][0][
                "output"] = 'No fue posible realizar la descarga del archivo correctamente: {}'.format(e)
        except TimeoutException as e:
            jsonEval["steps"][3]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][3]["status"] = jsonConst.FAILED
            jsonEval["steps"][3]["output"][0][
                "output"] = 'No fue posible realizar la descarga del archivo correctamente: {}'.format(e)

        if tiempo_step_inicio == 0:
            tiempo_step_inicio = Temporizador.obtener_tiempo_timer()

        tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
        fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
        jsonEval["steps"][3]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
        jsonEval["steps"][3]["start"] = fecha_inicio
        jsonEval["steps"][3]["end"] = fecha_fin

        return jsonEval

    def borrar_archivo_claro_drive(self, webdriver_test_ux: WebDriver, jsonEval, nombre_archivo_sin_ext: str,
                                   ext_archivo: str):
        # verifica que se haya iniciado sesion correctamente
        inicio_de_sesion_correcta = True if jsonEval["steps"][0]["status"] == jsonConst.SUCCESS else False

        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        # verifica que se haya iniciado sesion correctamente
        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_sesion(jsonEval):
            jsonEval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecto(jsonEval, tiempo_step_inicio,
                fecha_inicio, 3, 'No fue posible realizar el borrado del archivo. No se ingreso a la sesion de Claro '
                    'Drive correctamente')

            return jsonEval

        try:
            webdriver_test_ux.refresh()

            archivo_por_eliminar = WebDriverWait(webdriver_test_ux, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//span[@class="name-without-extension"][text()="{} "]'.format(nombre_archivo_sin_ext))))

            archivo_por_eliminar.click()

            btn_borrar = WebDriverWait(webdriver_test_ux, 20).until(EC.element_to_be_clickable(
                (By.XPATH, '//input[@type="button"][@class="menuItem svg deleteImage icon-delete icon-32"]')))

            btn_borrar.click()


            jsonEval["steps"][4]["output"][0]["status"] = jsonConst.SUCCESS
            jsonEval["steps"][4]["status"] = jsonConst.SUCCESS
            jsonEval["steps"][4]["output"][0]["output"] = 'Se realiza el borrado del archivo correctamente'
        except NoSuchElementException as e:
            jsonEval["steps"][4]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][4]["status"] = jsonConst.FAILED
            jsonEval["steps"][4]["output"][0][
                "output"] = 'No fue posible realizar el borrado del archivo correctamente: {}'.format(e.msg)

        except ElementClickInterceptedException as e:
            jsonEval["steps"][4]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][4]["status"] = jsonConst.FAILED
            jsonEval["steps"][4]["output"][0][
                "output"] = 'No fue posible realizar el borrado del archivo correctamente: {}'.format(e.msg)

        except TimeoutException as e:
            jsonEval["steps"][4]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][4]["status"] = jsonConst.FAILED
            jsonEval["steps"][4]["output"][0][
                "output"] = 'No fue posible realizar el borrado del archivo correctamente: {}'.format(e.msg)

        tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
        fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
        jsonEval["steps"][4]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
        jsonEval["steps"][4]["start"] = fecha_inicio
        jsonEval["steps"][4]["end"] = fecha_fin

        return jsonEval

    def cerrar_sesion_claro_drive(self, webdriver_test_ux: WebDriver, jsonEval):
        # verifica que se haya iniciado sesion correctamente
        inicio_de_sesion_correcta = True if jsonEval["steps"][0]["status"] == jsonConst.SUCCESS else False

        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        # verifica que se haya iniciado sesion correctamente
        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_sesion(jsonEval):
            jsonEval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecto(jsonEval, tiempo_step_inicio,
                fecha_inicio, 4, 'No fue posible realizar el cierre de sesion. No se ingreso a la sesion de Claro '
                    'Drive correctamente')

            return jsonEval

        try:
            webdriver_test_ux.refresh()
            boton_ajustes = WebDriverWait(webdriver_test_ux, 10).until(EC.element_to_be_clickable((By.ID, 'expand')))
            boton_ajustes.click()

            boton_cerrar_sesion = WebDriverWait(webdriver_test_ux, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//li[@data-id="logout"]/a')))

            boton_cerrar_sesion.click()
            WebDriverWait(webdriver_test_ux, 10).until(EC.presence_of_element_located((By.ID, 'login')))

            jsonEval["steps"][5]["output"][0]["status"] = jsonConst.SUCCESS
            jsonEval["steps"][5]["status"] = jsonConst.SUCCESS
            jsonEval["steps"][5]["output"][0]["output"] = 'Se cierra sesion correctamente'

        except NoSuchElementException as e:
            jsonEval["steps"][5]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][5]["status"] = jsonConst.FAILED
            jsonEval["steps"][5]["output"][0]["output"] = 'No fue posible realizar el cierre de sesion: {}'.format(
                e.msg)

        except ElementClickInterceptedException as e:
            jsonEval["steps"][5]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][5]["status"] = jsonConst.FAILED
            jsonEval["steps"][5]["output"][0]["output"] = 'No fue posible realizar el cierre de sesion: {}'.format(
                e.msg)

        except TimeoutException as e:
            jsonEval["steps"][5]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][5]["status"] = jsonConst.FAILED
            jsonEval["steps"][5]["output"][0]["output"] = 'No fue posible realizar el cierre de sesion: {}'.format(
                e.msg)

        except ElementNotInteractableException as e:
            jsonEval["steps"][5]["output"][0]["status"] = jsonConst.FAILED
            jsonEval["steps"][5]["status"] = jsonConst.FAILED
            jsonEval["steps"][5]["output"][0]["output"] = 'No fue posible realizar el cierre de sesion: {}'.format(
                e.msg)

        tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
        fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
        jsonEval["steps"][5]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
        jsonEval["steps"][5]["start"] = fecha_inicio
        jsonEval["steps"][5]["end"] = fecha_fin

        return jsonEval
