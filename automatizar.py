import pandas as pd
import matplotlib.pyplot as plt

#leer un archivo excel
df=pd.read_excel('ventas.xlsx')

#filtrar datos
#ventas_mayores=df[df['Coste unitario']>1000]

#crear grafico de barras por categoria
df.groupby('Zona')['Coste unitario'].sum().plot(kind='bar')
plt.title('Costo por Zona')
plt.xlabel('Zona')
plt.ylabel('Total Coste unitario')

#guardar en un nuevo archivo
#resumen.to_excel('resumen_costos.xlsx')

#guardar el grafico
plt.savefig('coste_zona.png')

print("guardado como coste_zona.png")



def extraer_ofertas():
    # Hacer petición HTTP
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraer los títulos de las ofertas laborales
    jobs = soup.find_all('h2', class_='fs18 fwB')  # Ajusta la clase según el sitio

    lista_ofertas = []
    for job in jobs:
        titulo = job.find('h2').text.strip()
        empresa = job.find('p', class_='company').text.strip()
        ubicacion = job.find('p', class_='location').text.strip()
        enlace = job.find('a')['href']

        lista_ofertas.append([titulo, empresa, ubicacion, enlace])

    # Guardar en un DataFrame de pandas
    df = pd.DataFrame(lista_ofertas, columns=['Título', 'Empresa', 'Ubicación', 'Enlace'])
    df.to_excel("reporte_ofertas.xlsx", index=False)
    
    return df

# 📩 Función para enviar el correo con el reporte
def enviar_correo():
    sender_email = "tucorreo@gmail.com"
    receiver_email = "destinatario@gmail.com"
    subject = "Reporte Diario de Ofertas Node.js"
    body = "Adjunto el reporte diario con las ofertas laborales de Node.js. 📄"

    # Configurar el correo
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Enviar el correo
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, "TU_CONTRASEÑA")
        server.sendmail(sender_email, receiver_email, msg.as_string())

# 📅 Programar ejecución automática todos los días
def tarea_diaria():
    df = extraer_ofertas()
    #enviar_correo()
    print("✅ Reporte enviado con éxito.")

# Ejecutar el script todos los días a las 8 AM
#schedule.every().day.at("08:00").do(tarea_diaria)

# Loop para que siga ejecutándose
#while True:
    #schedule.run_pending()
    #time.sleep(60)  # Esperar 1 minuto antes de verificar nuevamente

tarea_diaria()