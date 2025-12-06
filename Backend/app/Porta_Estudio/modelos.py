from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

# Definimos los tipos de recursos posibles
class ResourceType(str, enum.Enum):
    PDF = "pdf"
    VIDEO = "video"
    LINK = "link"
    IMAGE = "image"

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(255), nullable=True)
    
    # Tipo de recurso (PDF, Video de Youtube, etc.)
    type = Column(Enum(ResourceType), nullable=False)
    
    # La URL del video o la ruta del archivo en tu servidor
    url_or_path = Column(String(500), nullable=False)
        
    # Relaciones
    materia_id = Column(Integer, ForeignKey("materias.id")) # Se conecta al módulo Reviews
    user_id = Column(Integer, ForeignKey("users.id"))       # Quien lo subió
    
    # Para acceder a los objetos
    materia = relationship("app.Reviews.models.Materia")
    uploader = relationship("app.Usuarios.models.User")