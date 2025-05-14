import pywhatkit as kit
import datetime
import time

# Lista de contactos con código de país
contactos = [
    "+51907056224",
    "+51994115161"
]

# Mensaje a enviar
mensaje = "Hola, este es un mensaje automático enviado desde Python."

# Obtener hora actual
ahora = datetime.datetime.now()
hora = ahora.hour
minuto = ahora.minute + 2  # empezamos en el minuto siguiente

# Enviar mensaje programado a cada contacto
for numero in contactos:
    try:
        # Ajustar hora y minuto si se pasa de 59
        if minuto >= 60:
            minuto -= 60
            hora += 1
            if hora >= 24:
                hora = 0

        kit.sendwhatmsg(numero, mensaje, hora, minuto, wait_time=30, tab_close=True)
        print(f"Mensaje programado para {numero} a las {hora}:{minuto:02d}")
        time.sleep(30)  # Esperar para evitar colisiones entre envíos
        minuto += 2  # Aumentar un minuto para el siguiente envío

    except Exception as e:
        print(f"Error al enviar a {numero}: {e}")
