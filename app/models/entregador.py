from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class Entregador(Base):
    __tablename__ = "deliverers"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    tipo_veiculo = Column(String, nullable=False)
    capacidade_kg = Column(Float, nullable=False)
    disponivel = Column(Boolean, default=True)
