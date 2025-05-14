from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Ruta del Edge WebDriver
#EDGE_DRIVER_PATH = "C:\\WebDriver\\msedgedriver.exe"

# Configurar Edge
'''
options = Options()
options.add_argument("--headless")  # Ejecuta en segundo plano
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
'''
options = Options()
options.add_argument("--headless=new")  # Nueva forma de modo headless
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")  # Evita detección como bot
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)


# Configurar el WebDriver de Edge
service = Service("C:\\WebDriver\\msedgedriver.exe")
driver = webdriver.Edge(service=service)
# Inicializar WebDriver con Edge
#service = Service(EDGE_DRIVER_PATH)
driver = webdriver.Edge(service=service, options=options)

# URL del sitio de empleos
URL = "https://pe.computrabajo.com/trabajo-de-node-developer"
driver.get(URL)

# Esperar que la página cargue hasta que haya al menos un resultado
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "box_offer"))
    )
except:
    print("No se encontraron ofertas.")
    driver.quit()
    exit()

# Extraer los datos de las ofertas laborales
ofertas = driver.find_elements(By.CLASS_NAME, "box_offer")

lista_ofertas = []
for oferta in ofertas:
    try:
        titulo = oferta.find_element(By.TAG_NAME, "h2").text.strip()
        empresa = oferta.find_element(By.CLASS_NAME, "t_ellipsis").text.strip()
        ubicacion = oferta.find_element(By.CLASS_NAME, "fs16").text.strip()
        enlace = oferta.find_element(By.CLASS_NAME, "js-o-link").get_attribute("href")

        lista_ofertas.append([titulo, empresa, ubicacion, enlace])
    except Exception as e:
        print(f"Error procesando oferta: {e}")
        continue

# Guardar en un DataFrame de pandas
df = pd.DataFrame(lista_ofertas, columns=['Título', 'Empresa', 'Ubicación', 'Enlace'])

# Verificar si hay datos antes de guardar
if not df.empty:
    df.to_excel("C:\\Users\\brayan\\Desktop\\reporte_ofertas.xlsx", index=False)
    print("✅ Se guardó el archivo Excel en el escritorio.")
else:
    print("⚠️ No se encontraron datos para guardar.")

# Cerrar el navegador
driver.quit()
