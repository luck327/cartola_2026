import requests
import pandas as pd
from pathlib import Path

BASE_URL = "https://api.cartolafc.globo.com"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
OUTFILE = Path("teste_mercado_rodada_2.xlsx")

def testar_mercado():
    print("🚀 Acessando API do Mercado...")
    response = requests.get(f"{BASE_URL}/atletas/mercado", headers=HEADERS)
    
    if response.status_code != 200:
        print(f"❌ Erro na API: {response.status_code}")
        return

    data = response.json()
    atletas = data.get("atletas", [])
    
    # Criando a lista com os dados focados na Rodada 2
    lista_mercado = []
    for a in atletas:
        lista_mercado.append({
            "ID": a.get("atleta_id"),
            "Apelido": a.get("apelido"),
            "Preço_Atual": a.get("preco_num"),
            "Variação": a.get("variacao_num"),
            "Média": a.get("media_num"),
            "Status_ID": a.get("status_id"), # 7 é 'Provável'
            "Clube_ID": a.get("clube_id")
        })

    df = pd.DataFrame(lista_mercado)
    
    # Ordenar pelos mais caros para ver se os dados fazem sentido
    df = df.sort_values(by="Preço_Atual", ascending=False)

    df.to_excel(OUTFILE, index=False)
    print(f"✅ Sucesso! {len(df)} atletas mapeados.")
    print(f"📂 Arquivo gerado: {OUTFILE.resolve()}")

if __name__ == "__main__":
    testar_mercado()