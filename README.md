# Job Radar

Sistema automatizado de coleta, estruturação e análise de vagas de emprego. O projeto implementa um pipeline de Engenharia de Dados assíncrono utilizando a Arquitetura Medallion (Camadas Bronze, Silver e Gold), armazenamento relacional idempotente em PostgreSQL e modelagem de dados para futuras integrações de Inteligência Artificial.

O projeto reflete a evolução arquitetônica da Fase 2, incluindo as camadas Medallion, as migrações automatizadas com Alembic e o pipeline de carga idempotente.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.12+ (Asyncio, BeautifulSoup, Requests)
- **Banco de Dados:** PostgreSQL (containerizado)
- **ORM & Migrações:** SQLAlchemy e Alembic
- **Padrões & Arquitetura:** Medallion Architecture, CI/CD (GitHub Actions), Clean Code

## ⚙️ Pré-requisitos
- Python 3.12+
- Docker e Docker Compose plugin

## 🚀 Como rodar o ambiente de desenvolvimento local

**1. Configure o ambiente Python**
Crie e ative o ambiente virtual (`.venv`) para isolar as dependências do projeto:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Suba o banco de dados (Infraestrutura)**
O PostgreSQL rodará de forma isolada via Docker na porta 5432, utilizando volumes nomeados para persistência.
```bash
docker compose up -d
```

**4. Construa a Camada Gold (Migrações)**
Utilize o Alembic para criar as tabelas e aplicar a estrutura relacional no banco de dados atual:
```bash
alembic upgrade head
```

**5. Execute o Pipeline de Coleta (Bronze/Silver)**
Realize a extração assíncrona das APIs (Greenhouse/Lever) e a normalização de dados (remoção de tags HTML e padronização):
```bash
python -m src.services.collector
```

**6. Execute a Carga de Dados (Gold)**
Insira os dados da camada Silver no PostgreSQL. O script utiliza lógica idempotente (`ON CONFLICT DO NOTHING` com SHA-256) para evitar duplicação de vagas:
```bash
python -m src.services.carga_banco
```

**7. Valide a integridade**
Rode os testes automatizados com Pytest para garantir o funcionamento do motor de dados:
```bash
pytest
```
