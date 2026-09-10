from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.entregador import EntregadorCreate, EntregadorUpdate, EntregadorResponse
from app.crud import entregador as crud_entregador

router = APIRouter(prefix="/entregadores", tags=["entregadores"])

@router.post("/", response_model=EntregadorResponse)
def criar(entregador: EntregadorCreate, db: Session = Depends(get_db)):
    return crud_entregador.criar_entregador(db, entregador)

@router.get("/{entregador_id}", response_model=EntregadorResponse)
def buscar(entregador_id: int, db: Session = Depends(get_db)):
    db_entregador = crud_entregador.buscar_entregador(db, entregador_id)
    if db_entregador is None:
        raise HTTPException(status_code=404, detail="Entregador não encontrado!")
    return db_entregador

@router.get("/", response_model=list[EntregadorResponse])
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_entregador.listar_entregadores(db, skip, limit)

@router.put("/{entregador_id}", response_model=EntregadorResponse)
def atualizar(entregador_id: int, entregador: EntregadorUpdate, db: Session = Depends(get_db)):
    db_entregador = crud_entregador.atualizar_entregador(db, entregador_id, entregador)
    if db_entregador is None:
        raise HTTPException(status_code=404, detail="Entregador não encontrado")
    return db_entregador

@router.delete("/{entregador_id}", response_model=EntregadorResponse)
def deletar(entregador_id: int, db: Session = Depends(get_db)):
    db_entregador = crud_entregador.deletar_entregador(db, entregador_id)
    if db_entregador is None:
        raise HTTPException(status_code=404, detail="Entregador não encontrado")
    return db_entregador

