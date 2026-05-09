from pydantic import BaseModel
from datetime import datetime
from app.models.comentarios import TipoComentario

class ComentarioCreate(BaseModel):
    titulo: str
    tipo: TipoComentario
    conteudo: str

class ComentarioResponse(BaseModel):
    id: int
    titulo: str
    tipo: TipoComentario
    conteudo: str
    created_at: datetime

    model_config = {"from_attributes": True}