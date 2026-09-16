from sqlalchemy.orm import Session
from app.models.entrega import Entrega
from app.models.produto import Produto
from app.models.entregador import Entregador
from app.schemas.entrega import EntregaCreate, EntregaUpdate

def criar_entrega(db: Session, entrega: EntregaCreate):
    produto = db.query(Produto).filter(Produto.id == entrega.produto_id).first()
    if not produto:
        return None
    if entrega.entregador_id is not None:
        entregador = db.query(Entregador).filter(Entregador.id == entrega.entregador_id).first()
        if not entregador:
            return None
    db_entrega = Entrega(**entrega.model_dump())
    db.add(db_entrega)
    db.commit()
    db.refresh(db_entrega)
    return db_entrega

def buscar_entrega(db: Session, entrega_id: int):
    return db.query(Entrega).filter(Entrega.id == entrega_id).first()

def listar_entregas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Entrega).offset(skip).limit(limit).all()

def atualizar_entrega(db: Session, entrega_id: int, dados: EntregaUpdate):
    db_entrega = buscar_entrega(db, entrega_id)
    if not db_entrega:
        return None
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(db_entrega, campo, valor)
    db.commit()
    db.refresh(db_entrega)
    return db_entrega

def deletar_entrega(db: Session, entrega_id: int):
    db_entrega = buscar_entrega(db, entrega_id)
    if not db_entrega:
        return None
    db.delete(db_entrega)
    db.commit()
    return db_entrega
