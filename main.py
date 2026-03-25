 ###.               DEPENDENCIAS 

import os
import threading
import time
import requests
import base64
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import uvicorn
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from groq import Groq
from vars_texto import vars_texto
#####.              VARIABLES 


###.    APLICACIONES

#. FASTAPI

app = FastAPI()


##. SELENIUM 

#
chrome_options = Options()

chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/bin/chromedriver")  # ruta explícita

user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Mobile Safari/537.36"

chrome_options.add_argument(f"user-agent={user_agent}")

driver = webdriver.Chrome(service=service, options=chrome_options)

URL_TRABAJO = "https://2captcha.com/play-and-earn"

XPATH_INPUT = "/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/form[1]/div[1]/input[1]"

XPATH_BTN_SEND = "/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/form[1]/p[1]/button[2]"

XPATH_BTN_JUMP = "/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/form[1]/p[1]/button[1]"

XPATH_BTN_CANC = "/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/form[1]/button[1]"

XPATH_BTN_SOLVE = "/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/button[1]"

XPATH_LINK_START = "/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/section[2]/div[1]/div[2]/div[2]/a[1]"

XPATH_IFRAME = "/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/form[1]/div[1]/iframe[1]"

XPATH_DIV_BOX = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]"

vars_url = {"URL_TRABAJO":URL_TRABAJO,"URL_X":"https://ejemplo.com"}


vars_xpath = {"XPATH_INPUT": XPATH_INPUT,"XPATH_BTN_SEND":XPATH_BTN_SEND,"XPATH_BTN_CANC":XPATH_BTN_CANC,"XPATH_BTN_JUMP":XPATH_BTN_JUMP,"XPATH_BTN_SOLVE":XPATH_BTN_SOLVE,"XPATH_LINK_START":XPATH_LINK_START,"XPATH_IFRAME":XPATH_IFRAME,"XPATH_DIV_BOX":XPATH_DIV_BOX}
 

#.      GROQ

API_KEY = os.getenv("GROK_API_KEY")

client_ia = Groq(api_key=API_KEY)


###.    GENERALES 


PUBLIC_URL = "https://gpt-test-tz9o.onrender.com"

REGISTRO = list()




###.               FUNCIONES GENERALES

def log(msg) -> None:
    REGISTRO.append("MAIN_BOT -> "+msg)

def keep_alive():
    url = PUBLIC_URL
        
    while True:
        try:
            requests.get(url, timeout=30)
        except Exception as e:
            log(f"Error en Keep_Alive: {str(e)}")
            pass
        time.sleep(60)

###.               CLASES 

class SeleniumBot:
    def __init__(self, driver, vars_url: dict, vars_xpath: dict, REGISTRO: list) -> None:
	    self.driver = driver
	    self.vars_url = vars_url
	    self.vars_xpath = vars_xpath
	    self.REGISTRO = REGISTRO 
		
    def log(self,msg) -> None:
    	self.REGISTRO.append("SELENIUM_BOT -> "+msg)
		
    def cargar_cookies(self) -> None:
        self.log("Cargando cookies...")
        path = Path("cookies.json")
        if path.exists():
            with open(path, "r") as f:
        	    data = json.load(f)
            self.driver.get("https://2captcha.com")
            self.driver.delete_all_cookies() 
            for c in data.get("cookies", []):
            	self.driver.add_cookie(c)
        self.driver.execute_script(f"""let localData = {json.dumps(data.get("localStorage", {}))};for (let key in localData) {{ localStorage.setItem(key, localData[key]); }};let sessionData = {json.dumps(data.get("sessionStorage", {}))};for (let key in sessionData) {{ sessionStorage.setItem(key, sessionData[key]); }}""") 
        self.driver.refresh()
        self.log("Cookies Cargadas")
        
        	
    def nav_trabajo(self) -> None:
	    self.log("Navegando a trabajo")
	    self.driver.get(self.vars_url["URL_TRABAJO"])
		
	
    def start_work(self) -> None:
	    self.log("Clicando enlace de iniciar a trabajar")
	    elem = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, self.vars_xpath["XPATH_LINK_START"])))
	    self.driver.execute_script("arguments[0].click();", elem)
		
    def take_screenshot(self) -> bytes:
     try:
        self.log("Esperando que cargue la pagina")
        time.sleep(5)
        self.log("Pagina Cargada")
     except Exception as e:
         self.log("Primer Boton no enontrado")
         self.log("Intentar buscar el segundo boton")
         try:
             WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, self.vars_xpath["XPATH_BTN_JUMP"]))
        )
             self.log("Pagina Cargada")
         except Exception as e:
            self.log(f"Error al esperar elemento: {str(e)}")
            return b""
        
     self.log("Tomando captura de pantalla")
     return self.driver.get_screenshot_as_png()
    
    def solve_xcaptcha(self) -> None:
        self.log("Resolviendo Xcaptcha")
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, self.vars_xpath["XPATH_IFRAME"]))
        element = self.driver.find_element(By.XPATH, self.vars_xpath["XPATH_DIV_BOX"])
        self.driver.execute_script("arguments[0].click();", element)
        self.driver.switch_to.default_content()
        
    def solve_inputcaptcha(self, texto) -> None:
        self.log("Resolviendo Input Captcha")
        input_element = self.driver.find_element(By.XPATH,self.vars_xpath["XPATH_INPUT"])
        self.driver.execute_script("""
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, input_element, texto)
        boton_element = self.driver.find_element(By.XPATH,self.vars_xpath["XPATH_BTN_SEND"])
        boton_element.click()
        
    def return_work(self) -> None:
        self.log("Clicando botón de iniciar a trabajar")
        elem = self.driver.find_element(By.XPATH,self.vars_xpath["XPATH_BTN_START"])
        self.driver.execute_script("arguments[0].click();",elem)
        
    def reboot(self) -> None:
        self.log("Reiniciando la aplicación el bot")
        self.cargar_cookies()
        self.nav_trabajo()
        self.start_work()
        
class GroqBot:
    def __init__(self, client_ia: Groq, vars_texto: dict, REGISTRO: list) -> "Inicia las variables de clase":
        self.client_ia = client_ia
        self.vars_texto = vars_texto
        self.REGISTRO = REGISTRO
    
    def log(self,msg) -> None:
        self.REGISTRO.append("GROQ_BOT -> "+msg)
        
    def consultar(self,png_image) -> dict:
        self.log("Convirtiendo Imagen a cadena de base64")    	
        img_base64 = base64.b64encode(png_image).decode("utf-8")
        self.log("Convirtiendo base64 a formato de url")
        data_url = f"data:image/jpeg;base64,{img_base64}"
        self.log("Creando consulta con prompt_predeterminado + imagen servida por bot_selenium")
        consulta = {"role": "user", "content":[{"type":"text", "text": self.vars_texto["PROMPT_PRINCIPAL"]},{"type": "image_url", "image_url":{"url": data_url}}]}
        self.log("Añadiendo consulta al historial")
        self.vars_texto["HISTORIAL"].append(consulta)
        self.log("Pasando consulta a la IA_Groq")   
        response = self.client_ia.chat.completions.create(
                model=self.vars_texto["MODEL_NAME"],
                messages=self.vars_texto["HISTORIAL"]
            )
        self.log("Obteniendo Respuesta de la IA_Groq")
        try:           
            reply = response.choices[0].message.content
            self.log(f"Respuesta de IA_GROQ: {eval(reply)}")
            
        except Exception as e:
            self.log(f"Error al intentar extraer respuesta: {str(e)}")
            return
        try:
            lista_historial = list(self.vars_texto["HISTORIAL"])
            lista_historial.pop()
            self.vars_texto["HISTORIAL"] = lista_historial
        except Exception as e:
        	log("Error al intentar eliminar el último elemento del historial")
        self.log("Se consultó correctamente a la IA_GROQ")
        return eval(reply)
       
               
def captcha_bot() -> "Acciones":
    try:
	    log("Intentar Cargar Cookies")
	    bot_selenium.cargar_cookies()
    except Exception as e:
        log("Error al cargar las cookies")
        return
    
    try:
        log("Intentar Navegar a web Trabajo")
        bot_selenium.nav_trabajo()
    except Exception as e:
        log("Error en la navegación ")
        return
    
    try:
        log("Intentar iniciar sesión de trabajo")
        bot_selenium.start_work()
    except Exception as e:
        log("Error al iniciar sesión de trabajo")
        return
    
    log("Iniciando Bucle While")
    while True:
        log("Tomando Captura de Pantalla")
        try:
            png_image = bot_selenium.take_screenshot()
        except Exception as e:
            log(f"Error al intentar screenshot: {str(e)}")
            break
        
        log("Consultando al modelo de IA Groq")
        try:
            respuesta = bot_ia.consultar(png_image)
        except Exception as e:
            log(f"Error al intentar consultar IA: {str(e)}")
            break
        
        if respuesta.keys()[0] == 1:
            try:
                log("Intentar Resolver Xcaptcha")
                bot_selenium.solve_xcaptcha()
            except Exception as e:
                log(f"Error al Intentar Resolver Xcaptcha: {str(e)}")
                break
            
        elif respuesta.keys()[0] in [2,3,4]:
            try:
                log("Intentar_Resolver_InputCaptcha")
                bot_selenium.solve_inputcaptcha(respuesta[respuesta.keys()[0]])
            except Exception as e:
                log("Error al Intentar_Resolver_InputCaptcha")
                break
           
        elif respuesta.keys()[0] in [5,7]:
            try:
                log("Intentar_Reiniciar_Bot")
                bot_selenium.reboot()
            except Exception as e:
                log("Error al Intentar_Reiniciar_Bot")
                break
        elif respuesta.keys()[0] == 6:
            try:
                log("Intentar_Reiniciar_Trabajo")
                bot_selenium.return_work()
            except Exception as e:
                log("Error al Intentar_Reiniciar_Trabajo")
                break
            
        elif respuesta.keys()[0] == 8:
            try:
                log("Intentar_Saltar_Captcha")
                bot_selenium.saltar_captcha()
            except Exception as e:
                log("Error al Intentar_Saltar_Captcha")
                break
        else:
            break
        	
        	
def main_bot():
    while True:
        try:
            log("Intentando Iniciar bot principal")
            captcha_bot()
        except Exception as e:
        	log(f"Error al Intentar Iniciar bot principal: {str(e)}")
        	pass
        time.sleep(300)
        
##### Objetos de Clase

bot_selenium = SeleniumBot(driver, vars_url, vars_xpath, REGISTRO)

bot_ia = GroqBot(client_ia, vars_texto, REGISTRO)        
        
###.               ENDPOINTS

@app.get("/")
def root():
    return {"status": 200}
	
	
@app.get("/logs")
def devolver_logs():
    return REGISTRO

    
    
###.               EJECUCION

#. HILOS

threading.Thread(target=keep_alive, daemon=True).start()
threading.Thread(target=main_bot, daemon=True).start()

#. PRINCIPAL



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))