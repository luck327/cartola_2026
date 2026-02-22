<img width="883" height="312" alt="image" src="https://github.com/user-attachments/assets/8c5c4a4a-9d51-4c72-8a5e-dcca9e358bfd" />

# ⚽ Cartola 2026: Engenharia de Dados de Alta Performance

Projeto de engenharia de dados que implementa um **Lakehouse** com dados públicos da API do Cartola FC, com ingestão incremental, armazenamento histórico no S3 e evolução para camadas analíticas (Bronze/Silver/Gold).

## 🎯 Objetivo
Construir um pipeline ponta a ponta que permita:
- ingestão incremental de dados do Cartola FC;
- armazenamento histórico estruturado;
- implementação prática de arquitetura Lakehouse/Medallion;
- preparação para analytics e machine learning.

## 🚀 Arquitetura do Projeto
Atualmente, a camada **RAW** está implementada e o projeto evolui para o padrão Medallion:

- **RAW (implementada):** JSON bruto no S3, com versionamento histórico.
- **Bronze (planejada):** padronização em Delta Lake e definição de schema.
- **Silver (planejada):** limpeza, tipagem e modelagem analítica.
- **Gold (planejada):** tabelas agregadas, dashboards e features para ML.

## 🛠️ Tech Stack
- **Linguagem:** Python 3.12
- **Nuvem:** AWS S3
- **Bibliotecas:** `boto3`, `requests`
- **Próximos passos:** Delta Lake + Databricks

## 🌐 Fonte de dados
API pública do Cartola FC:
- https://api.cartola.globo.com/

### Endpoints de fatos
- `/mercado/status`
- `/atletas/pontuados/{rodada}`
- `/partidas/{rodada}`

### Endpoints de dimensões
- `/clubes`
- `/posicoes`
- `/atletas/mercado`
- `/rodadas`

## 🗃️ Estratégia de armazenamento no S3 (RAW)
Bucket: `cartola-raw`

Particionamento adotado:
- **Fatos por rodada:**
  - `atletas_pontuados/rodada=N/`
  - `partidas/rodada=N/`
- **Dimensões por data de snapshot:**
  - `clubes/data=YYYY-MM-DD/`
  - `posicoes/data=YYYY-MM-DD/`
  - `atletas_mercado/data=YYYY-MM-DD/`
  - `rodadas/data=YYYY-MM-DD/`
- **Estado de execução:**
  - `control/pipeline_state.json`

## ⚙️ Lógica de ingestão
### Fatos (`extract_cartola.py`)
- consulta `mercado/status`;
- detecta rodada consolidada;
- processa apenas rodadas pendentes;
- grava no S3 de forma incremental;
- atualiza `pipeline_state.json`.

Características: **incremental**, **idempotente** e **append-only**.

### Dimensões (`extract_cartola_dimensions.py`)
- executa snapshots dos endpoints dimensionais;
- grava partição por data;
- evita sobrescrita quando snapshot já existe.

Características: **snapshot diário** com **versionamento por data**.

## 🧩 Modelo analítico (referência)
Resumo do desenho estrela (Star Schema) pensado para Silver/Gold:
- dimensões: atleta, clube, posição;
- fatos: mercado, pontuação e partidas.

Detalhes em: `map_endpoints.md`.

## 🗂️ Organização de pastas (atual)
- `src/cartola_pipeline/config`: configurações centralizadas.
- `src/cartola_pipeline/ingestion`: extrações da API (fatos e dimensões).
- `src/cartola_pipeline/utils`: utilitários de integração (S3, datas, etc.).
- `src/cartola_pipeline/bronze`, `silver`, `gold`: estrutura base para evolução das camadas.
- scripts de raiz (`extract_cartola.py`, `extract_cartola_dimensions.py`) permanecem como entrypoints de compatibilidade.


> 📌 Nota: o `Details.md` foi atualizado com os comandos corretos de execução e com o mapeamento para os módulos em `src/cartola_pipeline`.

## 📚 Documentação complementar
- `Details.md`: detalhamento técnico completo da arquitetura e estratégia de particionamento.
- `map_endpoints.md`: mapa de entidades e fatos para modelagem analítica.
