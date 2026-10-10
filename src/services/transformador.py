import json
import html
from bs4 import BeautifulSoup


import os 

path = "data/bronze"
os.makedirs(f"data/silver", exist_ok=True)

def parse_lever(vaga_bruta, nome_empresa, data_extracao):
    return {
        "id_vaga": vaga_bruta.get("id"),
        "titulo": vaga_bruta.get("text"),
        "empresa": nome_empresa,
        "fonte": "lever",
        "local":vaga_bruta.get("categories", {}).get("location"), 
        "remoto": vaga_bruta.get("workplaceType", "").lower() == "remote",
        "url": vaga_bruta.get("hostedUrl"), 
        "descricao_texto": vaga_bruta.get("descriptionPlain"),
        "data_extracao": data_extracao
    } 


def parse_greenhouse(vaga_bruta, nome_empresa, data_extracao):

    htmltext = vaga_bruta.get("content", "")
    html_desescapado = html.unescape(htmltext)
    texto_limpo = BeautifulSoup(html_desescapado, "html.parser").get_text(separator=" ", strip=True)
    
    return {
        "id_vaga": vaga_bruta.get("id"),
        "titulo": vaga_bruta.get("title"),
        "empresa": nome_empresa,
        "fonte": "greenhouse",
        "local": vaga_bruta.get("location", {}).get("name"),
        "remoto": True if "remote" in texto_limpo.lower() or "home based" in texto_limpo.lower() else False,
        "url": vaga_bruta.get("absolute_url"),
        "descricao_texto": texto_limpo,
        "data_extracao": data_extracao
    }

conteudo = os.listdir(path)

for arquivo in conteudo:
    if "lever" in arquivo:
        with open(f"{path}/{arquivo}", "r") as f:
            dados = json.load(f)
            nome_empresa = arquivo.split("_")[0]
            data_extracao = arquivo.split("_")[2].split(".")[0]
            dados_transformados = [parse_lever(vaga, nome_empresa, data_extracao) for vaga in dados]
            with open(f"data/silver/{nome_empresa}_lever_{data_extracao}.json", "w") as f2:
                json.dump(dados_transformados, f2, indent=4, ensure_ascii=False)
    elif "greenhouse" in arquivo:
        with open(f"{path}/{arquivo}", "r") as f:
            dados = json.load(f)
            nome_empresa = arquivo.split("_")[0]
            data_extracao = arquivo.split("_")[2].split(".")[0]
            dados_transformados = [parse_greenhouse(vaga, nome_empresa, data_extracao) for vaga in dados.get("jobs", [])]
            with open(f"data/silver/{nome_empresa}_greenhouse_{data_extracao}.json", "w") as f2:
                json.dump(dados_transformados, f2, indent=4, ensure_ascii=False)