
<img width="883" height="312" alt="image" src="https://github.com/user-attachments/assets/8c5c4a4a-9d51-4c72-8a5e-dcca9e358bfd" />

# ⚽ Cartola 2026: Engenharia de Dados de Alta Performance

Este projeto demonstra a construção de um **Data Lakehouse** completo na AWS, utilizando dados reais da API do Cartola FC 2026 para análise preditiva e estatística.

## 🚀 Arquitetura do Projeto
O projeto segue o padrão **Medallion Architecture**:

- **Bronze:** Ingestão de dados brutos via Lambda e armazenamento em Delta Lake (S3).
- **Silver:** Limpeza, tipagem e transformação de JSONs complexos em tabelas relacionais (Spark/Databricks).
- **Gold (Em progresso):** Tabelas agregadas para dashboards e modelos de Machine Learning.

## 🛠️ Tech Stack
- **Linguagem:** Python / PySpark
- **Nuvem:** AWS (S3, Lambda, Budgets)
- **Framework de Dados:** Delta Lake & Apache Spark
- **Ferramenta de Processamento:** Google Colab (Spark Local + S3 Connector)

## 🧠 Desafios Superados
- **Tratamento de JSONs dinâmicos:** Implementação de lógica de `Explode` e `MapType` para tratar campos onde o dado (ID) era o nome da coluna.
- **FinOps:** Monitoramento ativo de custos para operação 100% gratuita dentro do AWS Free Tier.


## 🗂️ Organização de Pastas (atual)
- `src/cartola_pipeline/config`: configurações centralizadas.
- `src/cartola_pipeline/ingestion`: extrações da API (fatos e dimensões).
- `src/cartola_pipeline/utils`: utilitários de integração (S3, datas, etc.).
- `docs/architecture_folders.md`: guia da estrutura adotada.
- Scripts de raiz permanecem como entrypoints de compatibilidade.
