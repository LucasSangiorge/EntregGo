from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoResponse
from app.crud import produto as crud_produto

router = APIRouter(prefix="/produtos", tags=["produtos"])

@router.post("/", response_model=ProdutoResponse)
def criar(produto: ProdutoCreate, db: Session = Depends(get_db)):
    return crud_produto.criar_produto(db, produto)

@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar(produto_id: int, db: Session = Depends(get_db)):
    db_produto = crud_produto.buscar_produto(db, produto_id)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto

@router.get("/", response_model=list[ProdutoResponse])
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_produto.listar_produtos(db, skip, limit)

@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar(produto_id: int, produto: ProdutoUpdate, db: Session = Depends(get_db)):
    db_produto = crud_produto.atualizar_produto(db, produto_id, produto)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto

@router.delete("/{produto_id}", response_model=ProdutoResponse)
def deletar(produto_id: int, db: Session = Depends(get_db)):
    db_produto = crud_produto.deletar_produto(db, produto_id)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto