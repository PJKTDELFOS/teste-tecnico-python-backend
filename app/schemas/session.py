from pydantic import BaseModel
from datetime import datetime
from app.models.session import SessionStatus

class SessionResponse(BaseModel):
    id: int
    status: SessionStatus
    start_at: datetime
    end_at: datetime | None = None

    model_config = {
        "from_attributes":True
    }

