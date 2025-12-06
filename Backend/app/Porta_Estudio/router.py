from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.Porta_Estudio import esquemas, crud
from app import dependencias
from app.Usuarios import esquemas as user_schemas

router = APIRouter()

@router.post("/", response_model=esquemas.ResourceResponse)
def upload_resource(
    resource: esquemas.ResourceCreate, 
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(dependencias.get_current_user)
):
    """Sube un nuevo recurso (link o referencia a archivo)"""
    return crud.create_resource(db=db, resource=resource, user_id=current_user.id)

@router.get("/materia/{materia_id}", response_model=List[esquemas.ResourceResponse])
def get_materia_resources(materia_id: int, db: Session = Depends(get_db)):
    """Obtiene todos los recursos de una materia específica"""
    return crud.get_resources_by_materia(db, materia_id=materia_id)