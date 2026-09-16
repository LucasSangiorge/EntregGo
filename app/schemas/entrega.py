from pydantic import BaseModel, ConfigDict
from datetime import datetime

class EntregaBase(BaseModel):
    produto_id: int
    entregador_id: int | None = None

class EntregaCreate(EntregaBase):
    pass

class EntregaUpdate(BaseModel):
    entregador_id: int | None = None
    status: str | None = None

class EntregaResponse(EntregaBase):
    id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)