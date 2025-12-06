from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # <--- AÑADIR ESTO
from sqlalchemy.orm import Session
from app.database import get_db
from app.Usuarios import esquemas, crud
from app import auth # Importamos auth
from app import dependencias

router = APIRouter()

@router.post("/register", response_model=esquemas.UserResponse)
def register_user(user: esquemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el email ya existe
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # 2. Crear el usuario nuevo
    return crud.create_user(db=db, user=user)


@router.post("/login", response_model=esquemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # NOTA: OAuth2PasswordRequestForm siempre tiene campos 'username' y 'password'.
    # Aunque nosotros usamos email, el formulario lo enviará en el campo 'username'.

    # 1. Buscamos al usuario por correo (usando form_data.username)
    user = crud.get_user_by_email(db, email=form_data.username)

    # 2. Verificamos contraseña
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Creamos el token
    access_token = auth.create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}

# ... (tu código anterior) ...

@router.get("/me", response_model=esquemas.UserResponse)
def read_users_me(current_user: esquemas.UserResponse = Depends(dependencias.get_current_user)):
    """
    Obtiene la información del usuario logueado actualmente.
    Requiere Token JWT.
    """
    return current_user