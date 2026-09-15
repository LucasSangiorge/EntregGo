from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Produto(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    peso_kg = Column(Float, nullable=False)
    altura_cm = Column(Float, nullable=False)
    largura_cm = Column(Float, nullable=False)
    profundidade_cm = Column(Float, nullable=False)
    cidade_origem = Column(String, nullable=False)
    cidade_destino = Column(String, nullable=False)