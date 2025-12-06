from pydantic import BaseModel
from typing import List, Optional

# --- PROFESORES ---
class ProfesorBase(BaseModel):
    nombre: str

class ProfesorCreate(ProfesorBase):
    pass

class Profesor(ProfesorBase):
    id: int
    class Config:
        from_attributes = True

# --- MATERIAS ---
class MateriaBase(BaseModel):
    nombre: str

class MateriaCreate(MateriaBase):
    pass

class Materia(MateriaBase):
    id: int
    class Config:
        from_attributes = True

# --- RESEÑAS ---
class ResenaBase(BaseModel):
    comentario: Optional[str] = None
    calificacion: float
    dificultad: int

class ResenaCreate(ResenaBase):
    profesor_id: int
    materia_id: int

class Resena(ResenaBase):
    id: int
    user_id: int
    profesor: Profesor # Incluimos info del profe
    materia: Materia   # Incluimos info de la materia
    
    class Config:
        from_attributes = True