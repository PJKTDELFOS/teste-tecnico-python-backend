from pydantic import BaseModel, field_validator
from datetime import datetime
from app.models.tasks import TipoTask

class TaskCreate(BaseModel):
    titulo: str
    tipo: TipoTask

class TaskClose(BaseModel):
    nota: int

    @field_validator("nota")
    @classmethod
    def valida_nota(cls, v):
        if not (1 <= v <= 5):
            raise ValueError("Nota deve ser entre 1 e 5")
        return v

class TaskUpdate(BaseModel):
    nota: int | None = None

    @field_validator("nota")
    @classmethod
    def valida_nota(cls, v):
        if v is not None and not (1 <= v <= 5):
            raise ValueError("Nota deve ser entre 1 e 5")
        return v

class TaskResponse(BaseModel):
    id: str
    titulo: str
    tipo: TipoTask
    nota: int | None
    opened_at: datetime
    closed_at: datetime | None

    model_config = {"from_attributes": True}