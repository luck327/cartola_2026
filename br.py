import requests
import pandas as pd
import json
from pathlib import Path

# Configurações básicas
BASE_URL = "https://api.cartolafc.globo.com"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
OUTFILE = Path("dados_completos_rodada_1.xlsx")

def get_data(endpoint):
    url = f"{BASE_URL}{endpoint}"
    print(f"Acessando: {url}...")
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erro ao acessar {endpoint}: {e}")
        return None

def main():
    # 1. Buscar o Mercado (onde estão os nomes e apelidos)
    dados_mercado = get_data("/atletas/mercado")
    if not dados_mercado or "atletas" not in dados_mercado:
        print("Erro ao carregar lista de nomes dos atletas.")
        return

    # Criar um DataFrame auxiliar de nomes
    df_nomes = pd.DataFrame(dados_mercado["atletas"])
    # Ficamos apenas com o ID, Apelido e Foto para o cruzamento
    df_nomes = df_nomes[["atleta_id", "apelido", "foto", "clube_id"]]

    # 2. Buscar as pontuações da Rodada 1
    dados_pontuacao = get_data("/atletas/pontuados/1")
    if not dados_pontuacao or "atletas" not in dados_pontuacao:
        print("Rodada 1 sem dados de pontuação disponíveis.")
        return

    # Organizar os IDs e Pontos
    lista_pontos = []
    for atleta_id, info in dados_pontuacao["atletas"].items():
        lista_pontos.append({
            "atleta_id": int(atleta_id), # Convertendo para número para bater com o mercado
            "pontuacao": info.get("pontuacao")
        })
    
    df_pontos = pd.DataFrame(lista_pontos)

    # 3. O "Pulo do Gato": Cruzar as duas tabelas (Merge)
    # Isso traz o nome/apelido para quem tem pontuação
    df_final = pd.merge(df_pontos, df_nomes, on="atleta_id", how="left")

    # 4. Salvar
    if not df_final.empty:
        # Reordenar colunas para ficar mais bonito
        colunas = ["atleta_id", "apelido", "pontuacao", "clube_id", "foto"]
        df_final = df_final[colunas]
        
        df_final.to_excel(OUTFILE, index=False)
        print(f"\n[SUCESSO] Arquivo '{OUTFILE}' gerado!")
        print(f"Agora você pode ver quem é o dono de cada pontuação.")
    else:
        print("\n[AVISO] Não foi possível cruzar os dados.")

if __name__ == "__main__":
    main()