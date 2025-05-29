import os

carpeta="C:/Users/brayan/Pictures/renombrados_img"
prefijo="img_"
extension=(".jpg",".jpeg",".png")

archivos=[]

for f in os.listdir(carpeta):
    if f.endswith(extension):
        archivos.append(f)
        
#Creacion del archivo  para deshacer renombrado
ruta_deshacer=os.path.join(carpeta,"deshacer.bat")


with open(ruta_deshacer,"w",encoding="utf-8") as deshacer_mem:

  for i,nombre_actual in enumerate(archivos,start=1):
      extension_actual=os.path.splitext(nombre_actual)[1]
      nuevo_nombre=f"{prefijo}{i:03}{extension_actual}"
      ruta_actual=os.path.join(carpeta,nombre_actual)
      ruta_nueva=os.path.join(carpeta,nuevo_nombre)
      os.rename(ruta_actual,ruta_nueva)
      deshacer_mem.write(f'rename "{nuevo_nombre}" "{nombre_actual}"\n')
  deshacer_mem.write("del \"%~f0\"\n")

print(f"Renombrado completo. Ejecuta el .bat que veras en la carpeta para revertir cambios en '{ruta_deshacer}'")

