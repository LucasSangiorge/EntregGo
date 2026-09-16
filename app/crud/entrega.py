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

# ↓↓↓ AS DUAS FUNÇÕES NOVAS ENTRAM AQUI, DEPOIS DE deletar_entrega ↓↓↓

VEICULOS_ORDEM = ["moto", "carro", "caminhao"]

def calcular_tipo_veiculo(peso_kg: float, maior_dimensao_cm: float) -> str:
    if peso_kg <= 10:
        tipo_por_peso = "moto"
    elif peso_kg <= 50:
        tipo_por_peso = "carro"
    else:
        tipo_por_peso = "caminhao"

    if maior_dimensao_cm <= 60:
        tipo_por_dimensao = "moto"
    elif maior_dimensao_cm <= 150:
        tipo_por_dimensao = "carro"
    else:
        tipo_por_dimensao = "caminhao"

    indice_peso = VEICULOS_ORDEM.index(tipo_por_peso)
    indice_dimensao = VEICULOS_ORDEM.index(tipo_por_dimensao)
    return VEICULOS_ORDEM[max(indice_peso, indice_dimensao)]

def atribuir_entregador(db: Session, entrega: Entrega):
    produto = db.query(Produto).filter(Produto.id == entrega.produto_id).first()
    maior_dimensao = max(produto.altura_cm, produto.largura_cm, produto.profundidade_cm)
    tipo_necessario = calcular_tipo_veiculo(produto.peso_kg, maior_dimensao)

    entregador = (
        db.query(Entregador)
        .filter(Entregador.tipo_veiculo == tipo_necessario, Entregador.disponivel == True)
        .first()
    )
    if entregador is None:
        return None

    entrega.entregador_id = entregador.id
    entrega.status = "em_transporte"
    entregador.disponivel = False
    db.commit()
    db.refresh(entrega)
    return entregador
