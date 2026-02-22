Essa é uma ideia brilhante. No mundo corporativo, chamamos isso de **Handover** ou **Data Lineage Document**. Se você parar hoje e voltar daqui a duas semanas, esse arquivo será a diferença entre terminar o projeto em 10 minutos ou perder duas horas tentando lembrar por que o código deu erro.

Aqui está o seu **Diário de Bordo** formatado em Markdown. Você pode criar um arquivo chamado `PROGRESSO.md` no seu projeto ou simplesmente colar isso em uma célula de texto (Markdown) no topo do seu Notebook.

---

# 🚀 Diário de Progresso: Pipeline Cartola Lakehouse

## 📍 Status Atual: **TRANSFORMAÇÃO SILVER (Em Curso)**

O projeto encontra-se na fase crítica de conversão dos dados brutos (Bronze) para dados estruturados (Silver). O motor de processamento Spark foi otimizado para lidar com restrições de memória do ambiente Colab.

---

## 📊 Checkpoint dos Endpoints (Bronze → Silver)

Até o momento, mapeamos **8 origens de dados** na Bronze. Abaixo está o inventário de progresso:

| Origem (Bronze) | Destino (Silver) | Status | Detalhes Técnicos |
| --- | --- | --- | --- |
| `clubes_delta` | `dim_clubes` | ✅ Concluído | Unpivot de colunas dinâmicas realizado. |
| `atletas_pontuados_delta` | `fct_atleta_pontuado` | 🔄 Processando | Extração de `apelido` e `pontuacao` corrigida. |
| `partidas_delta` | `fct_partidas` | ✅ Concluído | Explode de array de partidas realizado. |
| `posicoes_delta` | `dim_posicoes` | ✅ Concluído | Corrigido erro de "Column Unresolved" (IDs como colunas). |
| `atletas_mercado_delta` | `fct_atleta_mercado` | 🔄 Pendente | Mapeamento de `preco_num` e `variacao_num`. |
| `rodadas_delta` | `dim_rodadas` | ⏳ Pendente | Extração simples de metadados da rodada. |
| `mercado_status_delta` | `dim_status` | ⏳ Pendente | Cópia direta para consulta de status. |
| `scouts_detalhados` | - | 🧊 Backlog | Aguardando definição se será necessário na Gold. |

---

## 🛠️ Decisões Técnicas de Engenharia (O que aprendemos)

1. **Contrato de Dados:** Descobrimos via log de erro que o JSON do Cartola usa `apelido` para o nome do jogador e `pontuacao` para os pontos (diferente do esperado `pontos_num`).
2. **Gestão de Memória:** Implementamos `localCheckpoint()` na tabela de atletas para evitar o erro `Java Heap Space`. Isso quebra a linhagem do Spark e libera a RAM do Driver.
3. **Arquitetura:** Optamos pelo particionamento por `rodada` nas tabelas fato para facilitar filtros rápidos na camada Gold.
4. **Visualização:** O uso de `.toPandas()` foi limitado a `limit(50)` para não derrubar a sessão do Spark.

---

## 🎯 Próximos Passos (Onde retomar)

1. **Validar Célula 3:** Confirmar se as 7 tabelas foram salvas no S3 (Sinal verde: Mensagem "🚀 PIPELINE SILVER CONCLUÍDO").
2. **Construir Camada Gold:** Realizar o JOIN final entre `fct_atleta_pontuado`, `dim_clubes` e `dim_posicoes`.
3. **Análise de Valor:** Cruzar `fct_atleta_mercado` com `fct_atleta_pontuado` para descobrir o "Custo-Benefício" (Pontos por Cartoleta).

---

> **Nota de Atenção:** Se o ambiente for reiniciado, lembre-se de sempre executar a **Célula 1** para remontar a `SparkSession` com os pacotes Delta e S3, caso contrário, o Spark não reconhecerá o protocolo `s3a://`.

---