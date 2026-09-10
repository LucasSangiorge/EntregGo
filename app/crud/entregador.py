from sqlalchemy.orm import Session
from app.models.entregador import Entregador
from app.schemas.entregador import EntregadorCreate, EntregadorUpdate

def criar_entregador(db: Session, entregador: EntregadorCreate):
    db_entregador = Entregador(**entregador.model_dump())
    db.add(db_entregador)
    db.commit()
    db.refresh(db_entregador)
    return db_entregador

def buscar_entregador(db: Session, entregador_id: int):
    return db.query(Entregador).filter(Entregador.id == entregador_id).first()

def listar_entregadores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Entregador).offset(skip).limit(limit).all()

def atualizar_entregador(db: Session, entregador_id: int, dados: EntregadorUpdate):
    db_entregador = buscar_entregador(db, entregador_id)
    if not db_entregador:
        return None
    for campo, valor in dados.model_dump(exclude_unset= True).items():
        setattr(db_entregador, campo, valor)
    db.commit()
    db.refresh(db_entregador)
    return db_entregador

def deletar_entregador(db: Session, entregador_id: int):
    db_entregador = buscar_entregador(db, entregador_id)
    if not db_entregador:
        return None
    db.delete(db_entregador)
    db.commit()
    return db_entregador