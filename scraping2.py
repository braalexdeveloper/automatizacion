import requests
from bs4 import BeautifulSoup
import csv

'''
# URL de la página a extraer
url = "https://books.toscrape.com/"  

# Hacer la solicitud HTTP
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Analizar el HTML con BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar todos los títulos de libros (están dentro de <h3>)
    libros = soup.find_all("h3")

    # Imprimir los títulos
    for libro in libros:
        print(libro.a["title"])  # Extraer el atributo "title"
else:
    print("Error al obtener la página")
'''

for page in range(1, 3):  # Extraer 2 páginas
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    libros = soup.find_all("h3")
    for libro in libros:
        print(libro.a["title"])



# Abrir archivo en modo escritura
with open("libros.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Libro"])  # Encabezado

    for libro in libros:
        writer.writerow([libro.text.strip()])  # Guardar cada producto

