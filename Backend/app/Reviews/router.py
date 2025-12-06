from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.Reviews import esquemas, crud
from app import dependencias # Para proteger rutas
from app.Usuarios import esquemas as user_schemas # Para el tipo de dato del usuario

router = APIRouter()

# --- RUTAS DE PROFESORES ---
@router.post("/profesores/", response_model=esquemas.Profesor)
def crear_profesor(profesor: esquemas.ProfesorCreate, db: Session = Depends(get_db)):
    return crud.create_profesor(db=db, profesor=profesor)

@router.get("/profesores/", response_model=List[esquemas.Profesor])
def leer_profesores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_profesores(db, skip=skip, limit=limit)

# --- RUTAS DE MATERIAS ---
@router.post("/materias/", response_model=esquemas.Materia)
def crear_materia(materia: esquemas.MateriaCreate, db: Session = Depends(get_db)):
    return crud.create_materia(db=db, materia=materia)

@router.get("/materias/", response_model=List[esquemas.Materia])
def leer_materias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_materias(db, skip=skip, limit=limit)

# --- RUTAS DE RESEÑAS (¡LA PARTE IMPORTANTE!) ---
@router.post("/resenas/", response_model=esquemas.Resena)
def crear_resena(
    resena: esquemas.ResenaCreate, 
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(dependencias.get_current_user) # <--- SEGURIDAD
):
    """
    Crea una reseña. Requiere estar logueado (candado verde).
    El sistema asigna automáticamente el autor basado en el token.
    """
    return crud.create_resena(db=db, resena=resena, user_id=current_user.id)

@router.get("/resenas/", response_model=List[esquemas.Resena])
def leer_resenas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_resenas(db, skip=skip, limit=limit)