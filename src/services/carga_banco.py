from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from sqlalchemy.dialects.postgresql import insert
from src.models.models import Vaga

import os
engine = create_engine("postgresql+psycopg2://admin:adminpassword@localhost:5432/jobradar")
Session = sessionmaker(engine)


session = Session()

for filename in os.listdir("data/silver"):
    with open(f"data/silver/{filename}", "r") as f:
        dados = json.load(f)
        if not dados:
            continue

        instrucao_insercao = insert(Vaga).values(dados)
        instrucao_final = instrucao_insercao.on_conflict_do_nothing(
            index_elements=['hash_vaga']
        )
        session.execute(instrucao_final)

session.commit()
session.close()
print("Carga finalizada com sucesso!")
