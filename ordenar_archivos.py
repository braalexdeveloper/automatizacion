import os
import shutil
import getpass
import time
import threading

from tkinter import Tk,filedialog,Button,Label
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


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

def esperar_archivo_libre(ruta_archivo,intentos=10,espera=0.5):

    for _ in range(intentos):
        try:
            with open(ruta_archivo,"rb"):
                return True
        except (PermissionError,OSError):
            time.sleep(espera)
    return False


def ordenar_archivos(ruta):
    # Mover archivos a su carpeta correspondiente
    for archivo in os.listdir(ruta):
        ruta_archivo = os.path.join(ruta, archivo)

        if os.path.isfile(ruta_archivo) and archivo != "log_movimientos.txt":

            if not esperar_archivo_libre(ruta_archivo):
                print(f"No se pudo acceder al archivo {archivo} por que esta seindo utilizado")
                continue
            
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

class ManejadorEventos(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"Nuevo archivo detectado: {event.src_path}")
            ordenar_archivos(ruta)

# Crear carpetas si no existen
for carpeta in set(tipos_archivos.values()):
    ruta_carpeta = os.path.join(ruta, carpeta)
    os.makedirs(ruta_carpeta, exist_ok=True)

ordenar_archivos(ruta)

manejador_eventos=ManejadorEventos()
observador=Observer()
observador.schedule(manejador_eventos,ruta,recursive=False)
#observador.start()

def iniciar_observador():
    observador.start()

def finalizar_observacion():
    observador.stop()
    observador.join()
    ventana.quit()

ventana.deiconify()
ventana.title("Vigilancia de carpeta")
ventana.geometry("400x150")

Label(ventana,text=f"Vigilando la carpeta: \n{ruta}",wraplength=350).pack(pady=10)
Button(ventana,text="Detener vigilancia y salir",command=finalizar_observacion).pack(pady=10)

hilo_vigilancia=threading.Thread(target=iniciar_observador,daemon=True)
hilo_vigilancia.start()

ventana.mainloop()


'''
print(f"Vigilando la carpeta: {ruta}")
print("Preciona control + c para detener el programa")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Deteniendo vigilancia")
    observador.stop()


observador.join()
'''

