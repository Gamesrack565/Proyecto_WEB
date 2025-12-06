import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. Cargar las variables del archivo .env
load_dotenv()

# 2. Obtener las credenciales
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# 3. Construir la URL de conexión
# Formato: mysql+pymysql://usuario:contraseña@servidor/nombre_db
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# 4. Crear el motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 5. Crear la sesión (nuestra "puerta" para hablar con la DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 6. La clase base para nuestros modelos (Tablas)
Base = declarative_base()

# 7. Función de utilidad para obtener la DB en cada petición (Dependency Injection)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()