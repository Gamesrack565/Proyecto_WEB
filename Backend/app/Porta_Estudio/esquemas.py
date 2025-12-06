from pydantic import BaseModel
from typing import Optional
from app.Porta_Estudio.modelos import ResourceType

class ResourceBase(BaseModel):
    title: str
    description: Optional[str] = None
    type: ResourceType
    url_or_path: str

class ResourceCreate(ResourceBase):
    materia_id: int

class ResourceResponse(ResourceBase):
    id: int
    user_id: int
    materia_id: int

    class Config:
        from_attributes = True