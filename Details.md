# Cartola FC Lakehouse

Projeto de engenharia de dados que implementa um Lakehouse completo utilizando dados públicos do Cartola FC, com ingestão incremental, armazenamento em Data Lake (AWS S3) e futura modelagem utilizando Delta Lake e Databricks.

---

# Objetivo

Construir um pipeline de dados completo que permita:

- Ingestão incremental de dados do Cartola FC
- Armazenamento histórico estruturado
- Implementação prática da arquitetura Lakehouse
- Suporte futuro para análises e machine learning
- Demonstrar competências práticas em engenharia de dados

---

# Arquitetura

O projeto segue o paradigma Lakehouse com separação em camadas:

Cartola API
↓
RAW Layer (JSON - AWS S3)
↓
BRONZE Layer (Delta Lake - Databricks)
↓
SILVER Layer (Modelagem)
↓
GOLD Layer (Analytics / ML)


Atualmente, a camada RAW encontra-se implementada.

---

# Tecnologias Utilizadas

- Python 3.12
- AWS S3
- boto3
- Requests
- Databricks (planejado)
- Delta Lake (planejado)
- GitHub
- VS Code

---

# Fonte de Dados

API pública do Cartola FC:

https://api.cartola.globo.com/


Principais endpoints utilizados:

## Endpoints de Fatos

- `/mercado/status`
- `/atletas/pontuados/{rodada}`
- `/partidas/{rodada}`

## Endpoints de Dimensões

- `/clubes`
- `/posicoes`
- `/atletas/mercado`
- `/rodadas`

---

# Estrutura do Data Lake (RAW Layer)

Bucket:

cartola-raw


Estrutura:



cartola-raw/

atletas_pontuados/
rodada=1/
rodada=2/
rodada=3/

partidas/
rodada=1/
rodada=2/
rodada=3/

clubes/
data=YYYY-MM-DD/

posicoes/
data=YYYY-MM-DD/

atletas_mercado/
data=YYYY-MM-DD/

rodadas/
data=YYYY-MM-DD/

mercado_status/
data=YYYY-MM-DD/

control/
pipeline_state.json

---

# Estratégia de Particionamento

## Fatos

Particionados por rodada:

atletas_pontuados/rodada=N/
partidas/rodada=N/


Motivo:

- Permitir ingestão incremental
- Otimizar leitura no Spark
- Evitar reprocessamento

---

## Dimensões

Particionadas por data de extração:

clubes/data=YYYY-MM-DD/

posicoes/data=YYYY-MM-DD/

atletas_mercado/data=YYYY-MM-DD/

rodadas/data=YYYY-MM-DD/


Motivo:

- Permitir versionamento
- Permitir auditoria
- Garantir consistência histórica

---

# Scripts

## extract_facts.py

Responsável por:

- Consultar o endpoint `/mercado/status`
- Identificar última rodada consolidada
- Comparar com última rodada processada
- Processar apenas rodadas pendentes
- Armazenar dados no S3
- Atualizar controle de estado

Controle armazenado em:

cartola-raw/control/pipeline_state.json


Exemplo:

{
"ultima_rodada_processada": 3,
"ultima_execucao": "2026-02-14T19:07:49"
}


Características:

- Incremental
- Idempotente
- Append-only

---

## extract_dimensions.py

Responsável por:

- Extrair snapshots das dimensões
- Armazenar snapshots por data
- Evitar sobrescrita de snapshots existentes

Características:

- Snapshot diário
- Versionamento por data
- Sem necessidade de controle incremental

---

# Camadas da Arquitetura

## RAW Layer

Status: concluído

Características:

- JSON bruto
- Sem transformação
- Armazenamento histórico completo

---

## BRONZE Layer

Status: planejado

Objetivo:

- Converter JSON em Delta Lake
- Definir schema
- Garantir ACID transactions
- Permitir versionamento

---

## SILVER Layer

Status: planejado

Objetivo:

- Limpeza de dados
- Modelagem dimensional
- Criação de tabelas analíticas

Exemplos:

- dim_jogador
- dim_clube
- fact_pontuacao

---

## GOLD Layer

Status: planejado

Objetivo:

- Analytics
- Feature engineering
- Machine learning
- Dashboards

---

# Execução

## Criar ambiente virtual

python3 -m venv cartoleiro


## Ativar ambiente virtual

Mac/Linux: source cartoleiro/bin/activate

---

## Executar ingestão de fatos

python extract_cartola.py

---

## Executar ingestão de dimensões



python extract_dimensions.py


---

# Características do Pipeline

- Arquitetura Lakehouse
- Ingestão incremental
- Idempotência
- Particionamento otimizado
- Separação de responsabilidades
- Compatível com Spark e Delta Lake

---

# Próximos Passos

- Implementação da camada Bronze
- Conversão para Delta Lake
- Modelagem Silver
- Criação de tabelas analíticas Gold
- Integração com Databricks

---

# Autor

Projeto desenvolvido como estudo prático de engenharia de dados com foco em arquitetura Lakehouse, ingestão incremental e modelagem analítica.
