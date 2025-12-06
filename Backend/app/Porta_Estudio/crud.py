from sqlalchemy.orm import Session
from app.Porta_Estudio import modelos, esquemas

def create_resource(db: Session, resource: esquemas.ResourceCreate, user_id: int):
    db_resource = modelos.Resource(
        **resource.dict(),
        user_id=user_id
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def get_resources_by_materia(db: Session, materia_id: int):
    return db.query(modelos.Resource).filter(modelos.Resource.materia_id == materia_id).all()