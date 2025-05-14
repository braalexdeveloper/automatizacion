import os

#Obtener la ruta de la carpeta donde esten los archivos
carpeta_path=r"C:\Users\brayan\Documents\archivosejemplo"

#Obtener los archivos en al carpeta
archivos=os.listdir(carpeta_path)

#Prefijo que se agregará al nombre del archivo
prefijo="youtube_"

#Iteración a los archivos de la carpeta
for nombre_archivo in archivos:
    #Obtener ruta completa del archivo
    archivo_path=os.path.join(carpeta_path,nombre_archivo)

    #Validar  si es o no una carpeta en la carpeta principal
    if os.path.isfile(archivo_path):
        #Obtener el nuevo nombre
        nuevo_archivo=prefijo+nombre_archivo

        #Obtener ruta completa del nuevo archivo
        nuevo_archivo_path=os.path.join(carpeta_path,nuevo_archivo)

        #Renombrar el archivo
        os.rename(archivo_path,nuevo_archivo_path)
