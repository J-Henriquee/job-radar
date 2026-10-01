# Job Radar

Sistema automatizado de coleta e análise de vagas de emprego usando Python, PostgreSQL e processamento vetorial (Embeddings).

## Pré-requisitos
- Python 3.12+
- Docker e Docker Compose plugin

## Como rodar o ambiente de desenvolvimento local

**1. Suba o banco de dados (PostgreSQL)**
O banco rodará de forma isolada via Docker na porta 5432.
```bash
sudo docker compose up -d

2. Configure o ambiente Python
Crie e ative o ambiente virtual para isolar as dependências:

Bash
python3 -m venv venv
source venv/bin/activate

3. Instale as dependências

Bash
pip install -r requirements.txt

4. Valide a instalação
Rode os testes automatizados para garantir que o motor do projeto está funcionando:

Bash
pytest