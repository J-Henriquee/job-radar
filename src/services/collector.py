import httpx
import asyncio
import json

async def buscar_dados(nome_empresa: str, fonte: str) -> dict:

    async with httpx.AsyncClient() as client:
        try:
            if fonte == "greenhouse":
                r = await client.get(f"https://boards-api.greenhouse.io/v1/boards/{nome_empresa}/jobs")
            elif fonte == "lever":
                r = await client.get(f"https://api.lever.co/v0/postings/{nome_empresa}?mode=json")
            r.raise_for_status()
            dados = r.json()
            return {"empresa": nome_empresa, "fonte": fonte, "dados": dados}
            
        except httpx.HTTPStatusError as e:
            return {"erro": f"Mural da empresa {nome_empresa} não encontrado: {e}"}
        except json.JSONDecodeError:
            return {"erro": f"A empresa {nome_empresa} não retornou um JSON válido."}

board_tokens = ['canonical',
                'discord', 
                'gitlab',
                'reddit', 
                'nubank', 
                'stripe', 
                'youtube',
                'tiktok', 
                'pinterest']

empresas_lever = ['leverdemo', 'coursera', 'hopper', 'hopper', 'kpmg-new-zealand', 'atlassian']


async def orquestrador():
    tarefas_greenhouse = [buscar_dados(board_token, "greenhouse") for board_token in board_tokens]
    tarefas_lever = [buscar_dados(empresa, "lever") for empresa in empresas_lever]

    resultados = await asyncio.gather(*tarefas_greenhouse, *tarefas_lever)
    for resultado in resultados:
        if "erro" in resultado:
            print(resultado["erro"])
        else:
            print(f"Sucesso! Dados encontrados com as chaves: {list(resultado.keys())}")
    return resultados


asyncio.run(orquestrador())



