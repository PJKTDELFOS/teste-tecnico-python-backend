from pydantic import BaseModel, field_validator
from datetime import datetime
from app.models.tasks import TipoTask

class TaskCreate(BaseModel):
    titulo: str
    tipo: TipoTask

class TaskClose(BaseModel):
    nivel_foco: int

    @field_validator("nivel_foco")
    @classmethod
    def valida_nota(cls, v):
        if not (1 <= v <= 5):
            raise ValueError("Nota deve ser entre 1 e 5")
        return v

class TaskUpdate(BaseModel):
    nivel_foco: int | None = None

    @field_validator("nivel_foco")
    @classmethod
    def valida_nota(cls, v):
        if v is not None and not (1 <= v <= 5):
            raise ValueError("Nota deve ser entre 1 e 5")
        return v

class TaskResponse(BaseModel):
    id: str
    titulo: str
    tipo: TipoTask
    nivel_foco: int | None
    opened_at: datetime
    closed_at: datetime | None

    model_config = {"from_attributes": True}