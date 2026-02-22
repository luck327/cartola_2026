# 🚀 Diário de Progresso: Pipeline Cartola Lakehouse

## 📍 Status Atual: **CAMADA SILVER CONCLUÍDA & HIGIENIZADA**

O projeto avançou da fase de transformação para a fase de governança. Conseguimos domar os JSONs complexos da API do Cartola e agora temos uma fundação sólida em Delta Lake para análises avançadas. As tabelas estão limpas, tipadas e armazenadas no bucket dedicado `cartola-silver`.

---

## 📊 Checkpoint dos Endpoints (Bronze → Silver)

Mapeamos a estrutura e garantimos a integridade das tabelas fundamentais. O "JSON tóxico" foi convertido em tabelas relacionais eficientes.

| Origem (Bronze) | Destino (Silver) | Status | Detalhes Técnicos |
| --- | --- | --- | --- |
| `clubes_delta` | `dim_clubes` | ✅ Concluído | Unpivot de IDs dinâmicos via `struct(*)` e `MapType`. |
| `atletas_pontuados_delta` | `fct_atleta_pontuado` | ✅ Concluído | Limpeza de fotos/links. Extração de `apelido` e `pontos` (Double). |
| `partidas_delta` | `dim_partidas` | ✅ Concluído | **Resolvido erro de caracteres inválidos** via aliasing explícito. |
| `posicoes_delta` | `dim_posicoes` | ✅ Concluído | Corrigido erro de "Column Unresolved" via mapeamento agnóstico. |
| `atletas_mercado_delta` | `fct_atleta_mercado` | 🔄 Pendente | Mapeamento de `preco_num` e `variacao_num`. |
| `rodadas_delta` | `dim_rodadas` | ⏳ Pendente | Extração simples de metadados da rodada. |
| `mercado_status_delta` | `dim_status` | ⏳ Pendente | Cópia direta para consulta de status. |
| `scouts_detalhados` | - | 🧊 Backlog | Aguardando definição de necessidade na camada Gold. |

---

## 🛠️ Decisões Técnicas de Engenharia (O que aprendemos)

1. **Desintoxicação de Nomes (Delta Compliance):** O Delta Lake não aceita caracteres como espaços ou chaves em nomes de colunas. Implementamos um processo de limpeza usando `select` com `alias` manual, evitando o erro `DELTA_INVALID_CHARACTERS_IN_COLUMN_NAMES`.
2. **Abstração por Mapas (Anti-Pattern JSON):** Como a API do Cartola usa IDs como nomes de colunas, criamos uma lógica de `F.from_json` com `MapType` para transformar colunas horizontais em linhas (Verticalização), tornando o dado relacional.
3. **FinOps & Gestão de Custos:** - Implementação de **AWS Budgets** com limite de alerta em $0,01 para garantir o uso do Free Tier.
    - Centralização de camadas em buckets específicos para controle de Requests S3.
4. **Data Minimization:** Adotamos a prática de descartar campos não analíticos (URLs de imagens e metadados de sistema) logo na entrada da Silver para reduzir o custo de armazenamento e aumentar a performance dos Joins.
5. **Gestão de Memória (Colab/Spark):** Uso de `localCheckpoint()` para evitar o erro `Java Heap Space` em DataFrames com linhagem complexa.

---

## 🎯 Próximos Passos (Onde retomar)

1. **Inaugurar Camada Gold:** Realizar o JOIN final entre `fct_atleta_pontuado`, `dim_clubes`, `dim_posicoes` e `dim_partidas`.
2. **Análise de Valor:** Cruzar `fct_atleta_mercado` (quando pronto) com o desempenho para descobrir o "Custo-Benefício" (Pontos por Cartoleta).
3. **Automação:** Ajustar a Lambda de ingestão para organizar o `cartola-raw` de forma particionada por timestamp de extração.

---

> **Nota de Atenção:** Ao reiniciar a sessão no Google Colab, execute sempre a célula de configuração da SparkSession com os JARs do Delta e Hadoop-AWS, caso contrário, a leitura dos caminhos `s3a://` falhará.

---