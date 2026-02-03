# 🗺️ Mapa Mental de Dados - Projeto Cartola

Este documento descreve a arquitetura de dados (Star Schema) utilizada para extração e análise dos dados da API.

## 1. Tabelas de Dimensão (O "Quem" e "Onde")
*Tabelas descritivas que servem para dar contexto aos IDs.*

- **Dim_Atleta** (`/atletas/mercado`)
  - Atributos: `atleta_id`, `apelido`, `foto`, `posicao_id`.
- **Dim_Clube** (`/clubes`)
  - Atributos: `clube_id`, `nome`, `abreviacao`, `escudos`.
- **Dim_Posicao** (`/atletas/mercado` -> chave 'posicoes')
  - Atributos: `posicao_id`, `nome` (Goleiro, Zagueiro, etc).

---

## 2. Tabelas de Fato (O "O que aconteceu")
*Dados numéricos e métricas que variam a cada rodada.*

- **Fato_Mercado** (`/atletas/mercado`)
  - Métricas: `preco_num`, `variacao_num`, `media_num`.
  - Contexto: Registro do estado do mercado no momento da consulta.
- **Fato_Pontuacao** (`/atletas/pontuados/{rodada}`)
  - Métricas: `pontuacao` final da rodada, `scouts` detalhados.
  - Contexto: A "tabela verdade" histórica de performance.
- **Fato_Partida** (`/partidas/{rodada}`)
  - Atributos: Clubes envolvidos, local, data/hora e validade da partida.

---

## 💡 Notas de Implementação
- **Periodicidade:** Coletas durante a rodada capturam parciais. Coletas pós-fechamento capturam dados consolidados.
- **Relacionamentos:** O `atleta_id` é a chave primária que conecta a Dim_Atleta com as tabelas de Fato_Mercado e Fato_Pontuacao.