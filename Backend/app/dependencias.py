from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app import auth
from app.Usuarios import crud

# 1. Definimos de dónde saca el token el sistema (apunta a tu ruta de login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

# 2. Función para obtener el usuario actual basado en el token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodificamos el token
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Buscamos al usuario en la BD
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user