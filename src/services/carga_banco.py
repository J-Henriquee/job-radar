import os
import json
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from src.models.models import Vaga

engine = create_engine("postgresql+psycopg2://admin:adminpassword@localhost:5432/jobradar")
Session = sessionmaker(engine)
session = Session()

hoje = date.today()
hoje_str = hoje.strftime("%Y-%m-%d")
pares_sucesso = set()

try:
    for filename in os.listdir("data/silver"):
        if hoje_str not in filename:
            continue

        with open(f"data/silver/{filename}", "r") as f:
            dados = json.load(f)
            
            if not dados:
                continue

            for vaga_dict in dados:
                vaga_dict['ultima_vez_vista'] = hoje
                vaga_dict['status'] = 'aberta'
                pares_sucesso.add((vaga_dict['empresa'], vaga_dict['fonte']))

            dados_deduplicados = list({vaga['hash_vaga']: vaga for vaga in dados}.values())
            
            qtd_duplicatas = len(dados) - len(dados_deduplicados)
            if qtd_duplicatas > 0:
                print(f"⚠️ {qtd_duplicatas} ocorrências com o mesmo hash removidas no arquivo {filename}.")

            instrucao_insercao = insert(Vaga).values(dados_deduplicados)
            
            instrucao_final = instrucao_insercao.on_conflict_do_update(
                index_elements=['hash_vaga'],
                set_={
                    'ultima_vez_vista': instrucao_insercao.excluded.ultima_vez_vista,
                    'status': instrucao_insercao.excluded.status
                }
            )
            session.execute(instrucao_final)

    for empresa, fonte in pares_sucesso:
        session.query(Vaga).filter(
            Vaga.empresa == empresa,
            Vaga.fonte == fonte,
            Vaga.ultima_vez_vista < hoje,
            Vaga.status == 'aberta'
        ).update({"status": "fechada"}, synchronize_session=False)

    session.commit()
    print("Carga finalizada com sucesso!")

except Exception as e:
    session.rollback()
    raise e
finally:
    session.close()