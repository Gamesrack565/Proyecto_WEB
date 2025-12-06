#Importa la libreria oficial de Google Generative AI.
import google.generativeai as genai
#Importa las excepciones especificas de Google API para manejar errores de red/cuota.
from google.api_core import exceptions # <--- Faltaba esto
#Importa el modulo del sistema operativo para acceder a variables de entorno.
import os
#Importa el modulo JSON para procesar la respuesta estructurada de la IA.
import json
#Importa el modulo time para realizar pausas (sleep) entre intentos.
import time
#Importa la funcion para cargar variables desde un archivo .env.
from dotenv import load_dotenv

# 1. Configuración
#Carga las variables de entorno del archivo .env al sistema.
load_dotenv()
#Obtiene la clave de API de Gemini desde las variables de entorno.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

#Verifica si la clave API fue cargada correctamente.
if not GEMINI_API_KEY:
    #Si no hay clave, lanza un error y detiene el programa.
    raise ValueError("No se encontró GEMINI_API_KEY en el archivo .env")

#Configura la libreria de Google con la clave API obtenida.
genai.configure(api_key=GEMINI_API_KEY)

# Usamos el modelo 2.0 Flash (versión rápida y potente)
#Inicializa el modelo especifico 'gemini-2.0-flash'.
model = genai.GenerativeModel('gemini-2.0-flash')

# Configuración de lotes (Chunks)
#Define el tamano del lote: enviaremos 200 mensajes por peticion para optimizar costos y contexto.
BATCH_SIZE = 200  # Procesamos 200 mensajes por golpe para aprovechar la ventana de contexto

#Define una funcion auxiliar para analizar un lote con mecanismo de reintento automatico.
def analyze_batch_with_retry(messages_batch, max_retries=3):
    """Intenta analizar un lote. Si falla por límite o timeout, espera y reintenta."""
    
    #Convierte la lista de diccionarios (mensajes) en un solo string de texto formateado para el prompt.
    chat_text = "\n".join([f"ID:{m['id']}|Autor:{m['author']}|Mensaje:{m['message']}" for m in messages_batch])

    #Construye el prompt (instrucciones) para la IA, inyectando el texto del chat.
    prompt = f"""
    Eres un analista experto. Extrae reseñas de profesores de este chat.
    CHAT:
    ---
    {chat_text}
    ---
    INSTRUCCIONES:
    1. IGNORA preguntas o charlas.
    2. EXTRAE opiniones claras sobre profesores.
    3. DETECTA apodos (CastaGOAT, Tenorio, etc).
    4. CALIFICA (1-10) usando texto y EMOJIS (☠️=5, 🐐=10, 👏=8).
    
    RESPUESTA JSON (LISTA):
    [
        {{
            "profesor_nombre": "Nombre",
            "comentario": "Opinión",
            "calificacion": 9.0,
            "dificultad": 3,
            "autor_original_id": "ID_NUMERICO" 
        }}
    ]
    """

    #Inicia un bucle de intentos segun el maximo de reintentos configurado.
    for attempt in range(max_retries):
        #Intenta ejecutar la llamada a la API.
        try:
            #Envia el prompt al modelo y espera la respuesta.
            response = model.generate_content(prompt)
            #Limpia la respuesta de texto eliminando los bloques de codigo Markdown (```json ... ```).
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            #Si la respuesta esta vacia o es una lista vacia, devuelve una lista vacia inmediatamente.
            if not clean_text or clean_text == "[]":
                return []
            #Intenta convertir el texto limpio en un objeto JSON (lista de diccionarios) y lo devuelve.
            return json.loads(clean_text)

        # Atrapamos Timeout (504) y Sobrecarga (429/503)
        #Captura errores especificos de la API: Cuota excedida, Servicio no disponible o Tiempo agotado.
        except (exceptions.ResourceExhausted, exceptions.ServiceUnavailable, exceptions.DeadlineExceeded):
            #Calcula un tiempo de espera incremental (20s, 40s, 60s...) para dar tiempo al servidor a recuperarse.
            wait_time = 20 * (attempt + 1)
            #Imprime un mensaje de advertencia indicando que se va a esperar.
            print(f"Error de red/límite (429/504). Esperando {wait_time}s antes de reintentar...")
            #Pausa la ejecucion del programa por el tiempo calculado.
            time.sleep(wait_time)
            #Salta a la siguiente iteracion del bucle 'for' para reintentar.
            continue 
            
        #Captura cualquier otro error generico (ej. error de sintaxis JSON, error de logica).
        except Exception as e:
            #Imprime el error y devuelve una lista vacia para no romper todo el proceso.
            print(f"Error no recuperable en lote: {e}")
            return [] 
    
    #Si sale del bucle sin exito, indica que fallo el lote.
    print("Se agotaron los reintentos para este lote.")
    #Devuelve una lista vacia como fallo seguro.
    return []

#Define la funcion principal que orquesta todo el proceso de analisis.
def analyze_reviews(messages):
    """Función principal que orquesta la división en lotes"""
    
    # 1. Pre-procesamiento
    #Inicializa una lista para los mensajes limpios.
    clean_messages = []
    #Recorre los mensajes originales enumerandolos para asignar un ID temporal.
    for i, msg in enumerate(messages):
        #Filtra mensajes muy cortos (menos de 10 caracteres) que probablemente no sean reseñas.
        if len(msg['message']) > 10:
            #Crea una copia del mensaje para no modificar el original.
            msg_with_id = msg.copy()
            #Asigna un ID numerico secuencial (crucial para que la IA referencie el autor).
            msg_with_id['id'] = i 
            #Añade el mensaje procesado a la lista limpia.
            clean_messages.append(msg_with_id)

    #Inicializa la lista final donde se guardaran todas las reseñas encontradas.
    all_reviews = []
    #Cuenta el total de mensajes validos a procesar.
    total_messages = len(clean_messages)
    
    #Imprime un mensaje de inicio.
    print(f"--- Iniciando análisis de {total_messages} mensajes con IA (Modelo: gemini-2.0-flash) ---")

    # 2. Bucle de lotes
    #Itera sobre la lista de mensajes saltando de BATCH_SIZE en BATCH_SIZE (ej. 0, 200, 400...).
    for i in range(0, total_messages, BATCH_SIZE):
        #Crea el sub-grupo (lote) actual usando slicing de listas.
        batch = clean_messages[i : i + BATCH_SIZE]
        #Imprime el progreso actual.
        print(f"Procesando lote {i} a {i + len(batch)}...")
        
        #Llama a la funcion de analisis para este lote especifico.
        batch_reviews = analyze_batch_with_retry(batch)
        
        # 3. Recuperación robusta del autor (AQUÍ ESTABA EL ERROR)
        #Recorre cada reseña extraida por la IA en este lote.
        for review in batch_reviews:
            #Obtiene el ID que la IA sugirio como autor, o -1 si no existe.
            raw_id = review.get("autor_original_id", -1)
            #Inicializa el nombre del autor como desconocido por defecto.
            found_author = "Desconocido"

            #Intenta resolver quien es el autor real basandose en la respuesta de la IA.
            try:
                # CASO A: La IA obedeció y mandó un número (ID)
                #Intenta convertir el ID a entero (primero a string para asegurar compatibilidad).
                msg_id = int(str(raw_id)) # Convertimos a string primero por seguridad, luego a int
                #Busca en la lista original el mensaje que tenga ese ID exacto.
                original_msg = next((m for m in clean_messages if m['id'] == msg_id), None)
                #Si encuentra el mensaje original.
                if original_msg:
                    #Recupera el nombre real del autor desde el mensaje original.
                    found_author = original_msg["author"]

            #Si falla la conversion a entero (la IA devolvio texto en lugar de ID).
            except ValueError:
                # CASO B: La IA desobedeció y mandó el nombre/teléfono directamente
                # Buscamos si ese texto coincide con algún autor del lote actual
                # (Esto arregla el error del +52...)
                #Busca en el lote actual si algun autor coincide con el texto que devolvio la IA.
                found_msg = next((m for m in batch if m['author'] in str(raw_id)), None)
                #Si encuentra una coincidencia de texto.
                if found_msg:
                    #Asigna el autor encontrado.
                    found_author = found_msg["author"]
                else:
                    # Si no lo encontramos, usamos el raw_id como el nombre (mejor que nada)
                    #Usa lo que sea que la IA haya devuelto como nombre de autor.
                    found_author = str(raw_id)

            # Asignamos el autor final y limpiamos el diccionario
            #Guarda el nombre real del autor en el diccionario de la reseña.
            review["autor_original"] = found_author
            #Si existe la clave del ID temporal, la elimina para limpiar el JSON final.
            if "autor_original_id" in review: 
                del review["autor_original_id"]
            
            #Añade la reseña procesada a la lista maestra.
            all_reviews.append(review)

        # Pausa base
        #Espera 10 segundos entre lotes para evitar saturar la API incluso si no hay errores.
        time.sleep(10) 

    #Imprime el resumen final.
    print(f"--- Análisis finalizado. Se encontraron {len(all_reviews)} reseñas. ---")
    #Devuelve la lista completa de reseñas.
    return all_reviews