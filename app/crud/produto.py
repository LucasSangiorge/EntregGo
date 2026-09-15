from sqlalchemy.orm import Session
from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate,ProdutoUpdate

def criar_produto(db: Session, produto: ProdutoCreate):
    db_produto = Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def buscar_produto(db: Session, produto_id: int):
    return db.query(Produto).filter(Produto.id == produto_id).first()

def listar_produtos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Produto).offset(skip).limit(limit).all()

def atualizar_produto(db: Session, produto_id: int, dados: ProdutoUpdate):
    db_produto = buscar_produto(db, produto_id)
    if not db_produto:
        return None
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(db_produto, campo, valor)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def deletar_produto(db: Session, produto_id: int):
    db_produto = buscar_produto(db, produto_id)
    if not db_produto:
        return None
    db.delete(db_produto)
    db.commit()
    return db_produto