from sqlalchemy import Column, String, Boolean, Date, Text
from sqlalchemy.orm import declarative_base

# Essa é a classe base que diz ao SQLAlchemy: "O que herdar de mim, vai virar tabela"
Base = declarative_base()

class Vaga(Base):
    __tablename__ = 'vagas'  # Nome da tabela no banco de dados

    # A nossa chave primária (hash).
    hash_vaga = Column(String, primary_key=True)
    titulo = Column(String, nullable=False)
    id_vaga = Column(String, nullable=False)
    empresa = Column(String, nullable=False)
    fonte = Column(String, nullable=False)
    local = Column(String, nullable=True)
    remoto = Column(Boolean, nullable=False)
    url = Column(String, nullable=False)
    descricao_texto = Column(Text, nullable=False)
    data_extracao = Column(Date, nullable=False)
    status = Column(String, nullable=False, default='aberta')
    ultima_vez_vista = Column(Date, nullable=False)
    