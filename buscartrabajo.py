
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

EDGE_DRIVER_PATH = "C:\\WebDriver\\msedgedriver.exe"

# Opciones del navegador
options = Options()
options.add_argument("--headless=new")  
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")


# Inicializar WebDriver
service = Service(EDGE_DRIVER_PATH)
driver = webdriver.Edge(service=service, options=options)

# URL de Computrabajo
URL = "https://pe.computrabajo.com/trabajo-de-programador-web-en-lima"
driver.get(URL)

# Esperar a que la página cargue completamente
time.sleep(5)  # Tiempo extra para asegurarnos de que todo se cargue

# Imprimir el HTML de la página (para verificar si Selenium está viendo las ofertas)
#print(driver.page_source)  # <--- VERIFICA QUE APAREZCAN OFERTAS EN EL HTML

# Esperar a que las ofertas aparezcan
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//article[contains(@class, 'box_offer')]"))
    )
except:
    print("⚠️ No se encontraron ofertas. Intenta aumentar el tiempo de espera.")
    driver.quit()
    exit()

# Extraer datos de las ofertas laborales
ofertas = driver.find_elements(By.XPATH, "//article[contains(@class, 'box_offer')]")

lista_ofertas = []
for oferta in ofertas:
    try:
        titulo = oferta.find_element(By.XPATH, ".//h2/a").text.strip()
        enlace = oferta.find_element(By.XPATH, ".//h2/a").get_attribute("href")
        empresa = oferta.find_element(By.XPATH, ".//a[contains(@class, 't_ellipsis')]").text.strip()
        ubicacion = oferta.find_element(By.XPATH, ".//p[contains(@class, 'fs16')]").text.strip()

        lista_ofertas.append([titulo, empresa, ubicacion, enlace])
    except Exception as e:
        print(f"Error procesando oferta: {e}")
        continue

# Guardar en un DataFrame de pandas
df = pd.DataFrame(lista_ofertas, columns=['Título', 'Empresa', 'Ubicación', 'Enlace'])

# Verificar si hay datos antes de guardar
if not df.empty:
    df.to_excel("C:\\Users\\brayan\\Desktop\\ofertas_computrabajo.xlsx", index=False)
    print("✅ Se guardó el archivo Excel en el escritorio.")
else:
    print("⚠️ No se encontraron datos para guardar.")

# Cerrar el navegador
driver.quit()