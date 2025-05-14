import os
import shutil
import getpass

from tkinter import Tk,filedialog
from datetime import datetime


ventana=Tk()
ventana.withdraw()

usuario=getpass.getuser()


#Ruta donde se va ordenar los archivos
#ruta="C:/Users/brayan/Documents/archivos_ordenados"
ruta=filedialog.askdirectory(title="Seleccionar la carpeta a ordenar")

#Crear carpetas en destino sino existe

#tipos=["Imagenes","pdfs","words","psd","excel","txt"]
tipos_archivos = {
    ".jpg": "Imagenes",
    ".png": "Imagenes",
    ".pdf": "pdfs",
    ".docx": "words",
    ".psd": "psd",
    ".xlsx": "excel",
    ".txt": "txt"
}

# Crear carpetas si no existen
for carpeta in set(tipos_archivos.values()):
    ruta_carpeta = os.path.join(ruta, carpeta)
    os.makedirs(ruta_carpeta, exist_ok=True)

# Mover archivos a su carpeta correspondiente
for archivo in os.listdir(ruta):
    ruta_archivo = os.path.join(ruta, archivo)

    if os.path.isfile(ruta_archivo):
        _, extension = os.path.splitext(archivo)
        carpeta_destino = tipos_archivos.get(extension.lower())

        if carpeta_destino:
            #destino = os.path.join(ruta, carpeta_destino, archivo)

            #Obtener fecha de ultima modificación
            fecha_mod=datetime.fromtimestamp(os.path.getmtime(ruta_archivo))
            subcarpeta_fecha=fecha_mod.strftime("%Y-%m") # Formatea a "2025-04"

            #Crear la subcarpeta si no existe
            carpeta_tipo=os.path.join(ruta,carpeta_destino)
            carpeta_fecha=os.path.join(carpeta_tipo,subcarpeta_fecha)

            if not os.path.exists(carpeta_fecha):
                os.makedirs(carpeta_fecha)
            
            #Ruta destino final
            destino=os.path.join(carpeta_fecha,archivo)
            
            shutil.move(ruta_archivo, destino)
            
            with open(os.path.join(ruta,"log_movimientos.txt"),"a",encoding="utf-8") as log:
                log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Usuario:{usuario}- Movido: {archivo} ->{destino}\n")