from pydantic import BaseModel, EmailStr

# 1. Datos comunes
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    career: str

# 2. Lo que recibimos al CREAR un usuario (incluye password)
class UserCreate(UserBase):
    password: str

# 3. Lo que DEVOLVEMOS al frontend (nunca devolvemos la password)
class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True # Permite leer datos de SQLAlchemy

# ... (tus schemas anteriores: UserBase, UserCreate, UserResponse) ...

# 4. Lo que recibimos cuando alguien quiere hacer LOGIN
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 5. Lo que devolvemos cuando el login es exitoso (El Token)
class Token(BaseModel):
    access_token: str
    token_type: str