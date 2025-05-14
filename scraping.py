import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
import csv

# Configurar el WebDriver de Edge
service = Service("C:\\WebDriver\\msedgedriver.exe")
driver = webdriver.Edge(service=service)

url = "https://cuadromania.studiosanely.com/cuadros"
driver.get(url)

# Esperar dinámicamente a que la página cargue
wait = WebDriverWait(driver, 10)

try:
    for i in range(2):  # Iterar 2 veces para recorrer páginas
        print(f"\n--- Página {i+1} ---\n")

        # Esperar hasta que los productos carguen
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h5")))

        # Obtener datos con BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        nombres = soup.select('.product_content h5')
        precios = soup.find_all(class_='org_price')
        estados = soup.find_all(class_='rating_count')

        for n, p, e in zip(nombres, precios, estados):
            print(f'{n.text.strip()} // {p.text.strip()} // {e.text.strip()}')

        # Intentar hacer clic en el botón "Siguiente"
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@class='page-item']/a[@class='page-link' and @rel='next']")))

            # **Desplazar hasta el botón antes de hacer clic**
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_button)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@class='page-item']/a[@class='page-link' and @rel='next']")))  # Volver a esperar para asegurar

            # **Manejar posible intercepción del clic**
            try:
                next_button.click()
            except ElementClickInterceptedException:
                print("El clic fue interceptado, intentando nuevamente...")
                driver.execute_script("arguments[0].click();", next_button)  # Forzar clic con JavaScript

        except (NoSuchElementException, TimeoutException):
            print("No se encontró el botón de siguiente página o ya no hay más páginas.")
            break  # Salir del bucle si no hay más páginas

finally:
    driver.quit()  # Cerrar el navegador al finalizar

