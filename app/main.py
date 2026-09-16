from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import entregador, produto, entrega


Base.metadata.create_all(bind=engine)

app = FastAPI(title="EntregGo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    
)

app.include_router(entregador.router)
app.include_router(produto.router)
app.include_router(entrega.router)