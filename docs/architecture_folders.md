# Organização de Pastas (proposta aplicada)

## Objetivo
Estruturar o projeto para refletir o fluxo Medallion (Bronze/Silver/Gold), separando ingestão, configuração e utilitários.

## Estrutura
- `src/cartola_pipeline/config`: configurações centrais (bucket, endpoints).
- `src/cartola_pipeline/ingestion`: jobs de extração (fatos e dimensões).
- `src/cartola_pipeline/utils`: utilitários compartilhados (ex.: S3).
- `src/cartola_pipeline/bronze|silver|gold`: camadas do lakehouse (placeholders para evolução).
- `jobs/lambda` e `jobs/spark`: ponto de organização para execução por runtime.
- `tests/unit`: base para testes automatizados.
- `docs`: documentação técnica e arquitetural.

## Compatibilidade
Os scripts da raiz (`extract_cartola.py` e `extract_cartola_dimensions.py`) foram mantidos como entrypoints compatíveis, delegando para os módulos em `src/`.
