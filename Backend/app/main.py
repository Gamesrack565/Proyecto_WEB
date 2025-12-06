from fastapi import FastAPI
from app.database import engine, Base
from app.Usuarios import models as user_models
from app.Usuarios import router as user_router
from app.Reviews import models as review_models 
from app.Reviews import router as reviews_router
from app.Porta_Estudio import modelos as study_models 
from app.Porta_Estudio import router as study_router
from app.Chatbot import router as chatbot_router
from app.Analisis_IA import router as ai_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Portal Estudiantil ESCOM")



app.include_router(user_router.router, prefix="/api/users", tags=["Usuarios"])
app.include_router(reviews_router.router, prefix="/api/reviews", tags=["Reseñas"])
app.include_router(study_router.router, prefix="/api/study", tags=["Portal de Estudio"])
app.include_router(chatbot_router.router, prefix="/api/bot", tags=["Asistente Virtual"])
app.include_router(ai_router.router, prefix="/api/ai", tags=["IA Análisis"])

@app.get("/")
def read_root():
    return {"message": "API funcionando correctamente"}