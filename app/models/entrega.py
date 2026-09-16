from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base                       

class Entrega (Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    entregador_id = Column(Integer, ForeignKey("deliverers.id"), nullable=True)
    status = Column(String, default="pendente", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())