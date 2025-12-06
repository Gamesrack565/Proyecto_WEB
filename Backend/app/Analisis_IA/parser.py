#Importa el modulo 're' para trabajar con expresiones regulares (Regex).
import re

#Define la funcion que recibe el contenido del archivo de texto como un string.
def parse_whatsapp_chat(content: str):
    """
    Analiza el contenido de un archivo de texto de WhatsApp (Android/Web/iOS).
    Soporta mensajes multilínea.
    """
    #Inicializa una lista vacia para almacenar los diccionarios de mensajes procesados.
    parsed_messages = []
    
    # Regex mejorado para soportar tu formato (Android) y el de iOS
    # Opción 1 (Android/Web): 24/1/2025, 7:12 p. m. - Autor: Mensaje
    # Opción 2 (iOS): [24/1/2025, 7:12:00] Autor: Mensaje
    
    #Define el patron de busqueda. Explicacion rapida:
    # 1. Busca la fecha (dd/mm/yyyy).
    # 2. Busca la hora, soportando formatos de 24h o AM/PM.
    # 3. Busca el separador (guion '-' o corchete ']').
    # 4. Captura el nombre del autor hasta los dos puntos ':'.
    # 5. Captura el resto de la linea como el mensaje.
    pattern = r'^(?:\[?)(\d{1,2}/\d{1,2}/\d{2,4})[,\s].*?(\d{1,2}:\d{2}(?::\d{2})?(?:\s?[ap]\.?\s?m\.?)?)(?:\]?)\s(?:-|]?)\s(.*?):\s(.*)$'
    
    

    #Divide todo el contenido del archivo en una lista de lineas individuales.
    lines = content.split('\n')
    #Inicializa una variable temporal para construir el mensaje que se esta procesando actualmente.
    current_message = None
    
    #Inicia un bucle para recorrer cada linea del archivo.
    for line in lines:
        #Elimina espacios en blanco al inicio y final de la linea.
        line = line.strip()
        #Si la linea esta vacia despues de limpiar, salta a la siguiente iteracion.
        if not line:
            continue # Saltar líneas vacías
            
        # Filtrar mensajes de sistema (ej: "se unió", "cambió el ícono")
        # Si la línea NO tiene ": ", probablemente es sistema o continuación de mensaje
        
        #Intenta coincidir la linea actual con el patron de fecha y hora.
        match = re.match(pattern, line, re.IGNORECASE)
        
        #Si 'match' es verdadero, significa que la linea empieza con fecha/hora (es un NUEVO mensaje).
        if match:
            # --- ES UN NUEVO MENSAJE ---
            # Si ya teniamos un mensaje construyendose en la variable temporal...
            if current_message:
                # ...lo guardamos en la lista final antes de empezar el nuevo.
                parsed_messages.append(current_message)
            
            #Extrae los grupos capturados por el Regex: fecha, hora, autor y el texto del mensaje.
            date, time, author, message = match.groups()
            
            #Crea un nuevo diccionario para el mensaje actual.
            current_message = {
                #Combina fecha y hora en un solo string.
                "timestamp": f"{date} {time}",
                #Guarda el autor sin espacios extra.
                "author": author.strip(),
                #Guarda el contenido del mensaje sin espacios extra.
                "message": message.strip()
            }
        #Si NO hay coincidencia con el patron (la linea no empieza con fecha).
        else:
            #Verifica si hay un mensaje activo construyendose.
            if current_message:
                # Agregamos esta línea al mensaje anterior, insertando un salto de linea.
                current_message["message"] += f"\n{line}"
    
    #Al terminar el bucle, verifica si quedo un ultimo mensaje pendiente en la variable temporal.
    if current_message:
        #Lo anade a la lista final (de lo contrario, el ultimo mensaje del chat se perderia).
        parsed_messages.append(current_message)
            
    #Devuelve la lista completa de mensajes procesados.
    return parsed_messages