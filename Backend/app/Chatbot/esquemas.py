from pydantic import BaseModel

class PreguntaChat(BaseModel):
    texto: str

class RespuestaChat(BaseModel):
    respuesta: str