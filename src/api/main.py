from fastapi import FastAPI, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional



from src.models.models import Vaga
from src.api.schemas import VagaResponse

# 1. Configuração do Banco (A mesma que você usou no script de carga)
DATABASE_URL = "postgresql+psycopg2://admin:adminpassword@localhost:5432/jobradar"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(
    title='Job Radar API', 
    version='0.1.0',
    description='API para consulta e processamento de vagas de emprego'
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Job Radar API está online!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/vagas", response_model=list[VagaResponse])
def listar_vagas(
    skip: int = 0,
    limit: int = 100,
    empresa: Optional[str] = None,
    remoto: Optional[bool] = None,
    titulo: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Vaga)

    if empresa:
        query = query.filter(Vaga.empresa.ilike(f"%{empresa}%"))

    if remoto is not None:
        query = query.filter(Vaga.remoto == remoto)

    if titulo:
        query = query.filter(Vaga.titulo.ilike(f"%{titulo}%"))

    vagas = query.order_by(Vaga.data_extracao.desc()).offset(skip).limit(limit).all()
    
    return vagas

@app.get("/vagas/{hash_vaga}", response_model=VagaResponse)
def obter_vaga(hash_vaga: str, db: Session = Depends(get_db)):
    vaga = db.query(Vaga).filter(Vaga.hash_vaga == hash_vaga).first()
    if not vaga:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vaga com o hash '{hash_vaga}' não foi encontrada."
            )
    return vaga
