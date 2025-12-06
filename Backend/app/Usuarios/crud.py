from sqlalchemy.orm import Session
from app.Usuarios import models, esquemas
from app import auth # <--- Importamos nuestro nuevo módulo

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: esquemas.UserCreate):
    # Usamos la función de auth.py para encriptar
    hashed_password = auth.get_password_hash(user.password)
    
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password, # Guardamos la hash
        full_name=user.full_name,
        career=user.career
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user