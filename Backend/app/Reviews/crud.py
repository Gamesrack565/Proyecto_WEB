from sqlalchemy.orm import Session
from app.Reviews import models, esquemas

# --- PROFESORES ---
def get_profesores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Profesor).offset(skip).limit(limit).all()

def create_profesor(db: Session, profesor: esquemas.ProfesorCreate):
    db_profesor = models.Profesor(nombre=profesor.nombre)
    db.add(db_profesor)
    db.commit()
    db.refresh(db_profesor)
    return db_profesor

# --- MATERIAS ---
def get_materias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Materia).offset(skip).limit(limit).all()

def create_materia(db: Session, materia: esquemas.MateriaCreate):
    db_materia = models.Materia(nombre=materia.nombre)
    db.add(db_materia)
    db.commit()
    db.refresh(db_materia)
    return db_materia

# --- RESEÑAS ---
def get_resenas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Resena).offset(skip).limit(limit).all()

def create_resena(db: Session, resena: esquemas.ResenaCreate, user_id: int):
    # Aquí ocurre la magia: vinculamos la reseña con el ID del usuario
    db_resena = models.Resena(
        **resena.dict(), # Copia todos los campos (comentario, calif, ids...)
        user_id=user_id  # Agrega el ID del usuario automáticamente
    )
    db.add(db_resena)
    db.commit()
    db.refresh(db_resena)
    return db_resena


# En backend/app/reviews/crud.py

def get_profesor_by_name(db: Session, nombre: str):
    # Busca un profesor cuyo nombre contenga el texto (ej: "Tenorio" encuentra "Ing. Tenorio")
    # El ilike hace que no importen mayúsculas/minúsculas
    return db.query(models.Profesor).filter(models.Profesor.nombre.ilike(f"%{nombre}%")).first()