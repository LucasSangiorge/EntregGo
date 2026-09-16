from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.entrega import EntregaCreate, EntregaUpdate, EntregaResponse
from app.crud import entrega as crud_entrega

router = APIRouter(prefix="/entregas", tags=["entregas"])

@router.post("/", response_model=EntregaResponse)
def criar(entrega: EntregaCreate, db: Session = Depends(get_db)):
    db_entrega = crud_entrega.criar_entrega(db, entrega)
    if db_entrega is None:
        raise HTTPException(status_code=404, detail="Produto ou entregador informado não encontrado")
    return db_entrega

@router.get("/{entrega_id}", response_model=EntregaResponse)
def buscar(entrega_id: int, db: Session = Depends(get_db)):
    db_entrega = crud_entrega.buscar_entrega(db, entrega_id)
    if db_entrega is None:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")
    return db_entrega

@router.get("/", response_model=list[EntregaResponse])
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_entrega.listar_entregas(db, skip, limit)

@router.put("/{entrega_id}", response_model=EntregaResponse)
def atualizar(entrega_id: int, entrega: EntregaUpdate, db: Session = Depends(get_db)):
    db_entrega = crud_entrega.atualizar_entrega(db, entrega_id, entrega)
    if db_entrega is None:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")
    return db_entrega