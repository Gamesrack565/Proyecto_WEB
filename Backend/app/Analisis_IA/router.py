#Importa las clases necesarias de FastAPI para manejar rutas, subida de archivos y dependencias.
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
#Importa la Session de SQLAlchemy para interactuar con la base de datos.
from sqlalchemy.orm import Session
#Importa la funcion 'get_db' para obtener una sesion de BD.
from app.database import get_db
#Importa nuestros modulos personalizados: el limpiador (parser) y el analista de IA (analyzer).
from app.Analisis_IA import parser, analyzer
#Importa las funciones CRUD (Crear, Leer, Actualizar, Borrar) y los esquemas Pydantic.
from app.Reviews import crud, esquemas
#Importa los modelos de base de datos de las reseñas.
from app.Reviews import models as review_models 

#Crea una instancia del router de FastAPI.
router = APIRouter()

#Define el endpoint POST en '/process_reviews' para procesar el archivo.
@router.post("/process_reviews")
#Define la funcion asincrona, recibiendo el archivo y la sesion de BD.
async def process_reviews_file(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    """
    1. Recibe el chat.
    2. Lo limpia (Parser).
    3. Lo analiza con Gemini (Analyzer).
    4. Auto-registra profesores y guarda reseñas en la BD.
    """
    # 1. Validar archivo
    #Comprueba si el nombre del archivo termina en '.txt'.
    if not file.filename.endswith('.txt'):
        #Si no es txt, lanza un error HTTP 400.
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos .txt")
    
    # 2. Leer contenido
    #Lee el contenido binario del archivo de forma asincrona.
    content_bytes = await file.read()
    #Intenta decodificar los bytes a texto usando UTF-8 (estandar moderno).
    try:
        content_str = content_bytes.decode('utf-8')
    #Si falla la decodificacion (comun en archivos de Windows antiguos).
    except UnicodeDecodeError:
        # Intenta decodificar usando latin-1 (ISO-8859-1).
        content_str = content_bytes.decode('latin-1')
    
    # 3. Parsear (Limpiar formato WhatsApp)
    #Llama a nuestra funcion 'parser' para convertir el texto crudo en una lista de diccionarios limpios.
    clean_messages = parser.parse_whatsapp_chat(content_str)
    #Imprime en consola cuantos mensajes validos se detectaron.
    print(f"--- Chat cargado: {len(clean_messages)} mensajes detectados ---")
    
    #Si la lista de mensajes esta vacia (el formato del chat no era compatible).
    if not clean_messages:
        #Devuelve un mensaje de error controlado.
        return {"success": False, "message": "No se detectaron mensajes válidos. Revisa el formato."}

    # 4. Analizar (Inteligencia Artificial)
    #Envia los mensajes limpios a la IA (analyzer) para extraer las reseñas.
    extracted_reviews = analyzer.analyze_reviews(clean_messages)
    
    #Si la IA no encontro ninguna reseña en el chat.
    if not extracted_reviews:
        #Devuelve exito (porque el proceso funciono), pero avisa que no hubo datos.
        return {"success": True, "message": "La IA analizó el chat pero no encontró reseñas claras.", "data": []}

    #Inicializa una lista para guardar las reseñas que se inserten con exito.
    saved_reviews = []
    #Inicializa un contador para saber cuantos profesores nuevos se crearon.
    profesores_nuevos = 0
    
    # 5. Guardar en la Base de Datos
    #Define el ID de usuario que se usara como "autor" de estas reseñas automaticas.
    # Usamos un usuario ID 1 (Admin/Sistema) para estas reseñas automáticas
    SYSTEM_USER_ID = 1 
    
    #Imprime mensaje de inicio de guardado.
    print("--- Iniciando guardado en Base de Datos ---")

    #Recorre cada reseña extraida por la IA.
    for review_data in extracted_reviews:
        #Obtiene el nombre del profesor de los datos extraidos.
        nombre_profe = review_data['profesor_nombre']
        
        # A. Lógica de Auto-Registro de Profesor
        #Consulta en la BD si ya existe un profesor con ese nombre exacto.
        db_profesor = crud.get_profesor_by_name(db, nombre=nombre_profe)
        
        #Si el profesor NO existe en la BD.
        if not db_profesor:
            #Imprime que se va a registrar uno nuevo.
            print(f"🆕 Registrando nuevo profesor: {nombre_profe}")
            #Crea el esquema Pydantic para el nuevo profesor.
            nuevo_profe_schema = esquemas.ProfesorCreate(nombre=nombre_profe)
            #Llama al CRUD para insertar el profesor en la BD y obtiene el objeto creado.
            db_profesor = crud.create_profesor(db=db, profesor=nuevo_profe_schema)
            #Incrementa el contador de profesores nuevos.
            profesores_nuevos += 1
        
        # B. Guardar la Reseña vinculada a ese Profesor
        #Obtiene el ID real del profesor (ya sea el encontrado o el recien creado).
        real_profesor_id = db_profesor.id

        

        # Preparamos el comentario agregando el autor original para referencia
        #Concatena el comentario de la IA con la fuente original (quien lo escribio en WhatsApp).
        texto_final = f"{review_data['comentario']}\n(Fuente: Chat WhatsApp - {review_data['autor_original']})"

        # --- PROTECCIÓN CONTRA VALORES NULOS ---
        #Obtiene la calificacion, o None si no existe.
        calif_final = review_data.get('calificacion')
        #Si la IA fallo y mando None.
        if calif_final is None:
            #Asigna un 7.0 como valor por defecto.
            calif_final = 7.0 
            
        #Obtiene la dificultad, o None si no existe.
        dificultad_final = review_data.get('dificultad')
        #Si la IA fallo y mando None.
        if dificultad_final is None:
            #Asigna un 3 como valor por defecto.
            dificultad_final = 3 

        #Crea el esquema Pydantic para la nueva reseña con todos los datos limpios.
        nueva_resena = esquemas.ResenaCreate(
            #Asigna el ID del profesor.
            profesor_id=real_profesor_id, 
            #Asigna un ID de materia generico (1) por defecto.
            materia_id=1,  
            #Asigna el texto final formateado.
            comentario=texto_final,
            #Convierte y asigna la calificacion a float.
            calificacion=float(calif_final), 
            #Convierte y asigna la dificultad a int.
            dificultad=int(dificultad_final) 
        )
        
        #Intenta guardar la reseña en la BD.
        try:
            #Llama al CRUD para crear la reseña, asociandola al usuario del sistema.
            saved = crud.create_resena(db=db, resena=nueva_resena, user_id=SYSTEM_USER_ID)
            #Anade la reseña guardada a la lista de exitos.
            saved_reviews.append(saved)
        #Si ocurre un error al guardar (ej. base de datos caida).
        except Exception as e:
            #Imprime el error especifico pero continua con la siguiente reseña.
            print(f"Error guardando reseña individual: {e}")
        
    #Devuelve un resumen final del proceso en formato JSON.
    return {
        "success": True,
        "message": f"Proceso finalizado. Se analizaron {len(clean_messages)} mensajes. Se encontraron {len(extracted_reviews)} opiniones. Se registraron {profesores_nuevos} profesores nuevos.",
        "data": extracted_reviews
    }