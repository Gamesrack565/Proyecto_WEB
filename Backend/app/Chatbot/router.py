#Importa las clases necesarias de FastAPI para enrutamiento y dependencias.
from fastapi import APIRouter, Depends
#Importa la Session de SQLAlchemy para realizar consultas a la base de datos.
from sqlalchemy.orm import Session
#Importa la funcion 'get_db' para obtener una sesion de base de datos activa.
from app.database import get_db
#Importa los esquemas (Pydantic) especificos para la entrada y salida del chatbot.
from app.Chatbot import esquemas
# Importamos los modelos de Reseñas para que el bot pueda "leer" la base de datos
# Asegúrate de usar el nombre correcto de tu carpeta (Reviews o reviews)
#Importa los modelos de base de datos (tablas) del modulo de Reseñas.
from app.Reviews import models as review_models 

#Crea una instancia del enrutador de FastAPI.
router = APIRouter()

#Define un endpoint POST en la ruta '/preguntar'.
#Usa el esquema 'RespuestaChat' para validar lo que el bot responde.
@router.post("/preguntar", response_model=esquemas.RespuestaChat)
#Define la funcion del endpoint, recibiendo la pregunta del usuario y la sesion de BD.
def preguntar_al_bot(pregunta: esquemas.PreguntaChat, db: Session = Depends(get_db)):
    #Convierte el texto de la pregunta a minusculas para facilitar la comparacion.
    texto = pregunta.texto.lower()
    
    # --- CONECTAR LA IA
    
    #Verifica si el usuario esta saludando.
    if "hola" in texto:
        #Devuelve un saludo predefinido.
        return {"respuesta": "¡Hola! Soy tu asistente de ESCOM. ¿En qué puedo ayudarte?"}
    
    #Verifica si el usuario pregunta por profesores o maestros.
    if "profesor" in texto or "maestro" in texto:
        # El bot busca en la base de datos si hay profesores registrados
        #Realiza una consulta a la tabla 'Profesor' para contar cuantos registros existen.
        count = db.query(review_models.Profesor).count()
        #Devuelve una respuesta dinamica con el dato real de la base de datos.
        return {"respuesta": f"Actualmente tengo información sobre {count} profesores registrados en el sistema."}
    
    #Verifica si el usuario pregunta por horarios.
    if "horario" in texto:
        #Devuelve una respuesta informativa sobre donde encontrar los horarios.
        return {"respuesta": "Puedes consultar la sección de Horarios y Calendarios en el menú principal."}

    # Respuesta por defecto
    #Si ninguna de las condiciones anteriores se cumple, devuelve un mensaje generico.
    return {"respuesta": "Aún estoy aprendiendo. Por favor, intenta preguntar sobre profesores o horarios."}