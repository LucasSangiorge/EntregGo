from pydantic import BaseModel, ConfigDict

class ProdutoBase(BaseModel):
    nome: str
    peso_kg: float
    altura_cm: float
    largura_cm: float
    profundidade_cm: float
    cidade_origem: str
    cidade_destino: str

class ProdutoCreate(ProdutoBase):
    pass 

class ProdutoUpdate(BaseModel):
    nome: str | None = None
    peso_kg: float | None = None
    altura_cm: float | None = None
    largura_cm: float | None = None
    profundidade_cm: float | None = None
    cidade_origem: str | None = None
    cidade_destino: str | None = None

class ProdutoResponse(ProdutoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)