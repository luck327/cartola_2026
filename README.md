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