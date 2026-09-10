from pydantic import BaseModel, ConfigDict

class EntregadorBase(BaseModel):
    nome: str
    tipo_veiculo: str
    capacidade_kg: float
    disponivel: bool = True

class EntregadorCreate(EntregadorBase):
    pass

class EntregadorUpdate(BaseModel):
    nome: str | None = None
    tipo_veiculo: str | None = None
    capacidade_kg: float | None = None
    disponivel: bool | None = None

class EntregadorResponse(EntregadorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

