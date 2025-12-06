from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

# --- CONFIGURACIÓN ---
# En un proyecto real, esto iría en tu .env
SECRET_KEY = "esta_es_una_clave_super_secreta_cambiala"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 

# Contexto de encriptación (usando Argon2 como configuramos)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# --- FUNCIONES ---

def verify_password(plain_password, hashed_password):
    """Compara una contraseña normal con la encriptada de la DB"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Encripta una contraseña"""
    return pwd_context.hash(password)

def create_access_token(data: dict):
    """Crea el Token JWT con tiempo de expiración"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt