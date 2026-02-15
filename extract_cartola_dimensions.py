import json
import requests
import boto3
from datetime import datetime, UTC

# =========================
# CONFIG
# =========================

BUCKET_NAME = "cartola-raw"

ENDPOINTS = {
    "clubes": "https://api.cartola.globo.com/clubes",
    "posicoes": "https://api.cartola.globo.com/posicoes",
    "atletas_mercado": "https://api.cartola.globo.com/atletas/mercado",
    "rodadas": "https://api.cartola.globo.com/rodadas"
}

s3 = boto3.client("s3")


# =========================
# UTIL FUNCTIONS
# =========================

def snapshot_ja_existe(endpoint_name, data_particao):
    prefix = f"{endpoint_name}/data={data_particao}/"
    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=prefix,
        MaxKeys=1
    )
    return "Contents" in response


def salvar_json(endpoint_name, data_particao, payload):
    timestamp = datetime.now(UTC).strftime("%Y-%m-%dT%H-%M-%S")

    key = (
        f"{endpoint_name}/"
        f"data={data_particao}/"
        f"extract_{timestamp}.json"
    )

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps(payload)
    )

    print(f"📦 Salvo em s3://{BUCKET_NAME}/{key}")


# =========================
# MAIN
# =========================

def main():

    hoje = datetime.now(UTC).date()

    print(f"📅 Executando snapshot de dimensões para {hoje}")

    for nome, url in ENDPOINTS.items():

        print(f"\n🔎 Processando endpoint: {nome}")

        if snapshot_ja_existe(nome, hoje):
            print(f"⚠️ Snapshot já existe para {nome} em {hoje}. Pulando.")
            continue

        response = requests.get(url)

        if response.status_code != 200:
            print(f"❌ Erro ao consultar {nome}")
            print(response.text)
            continue

        payload = response.json()

        salvar_json(nome, hoje, payload)

    print("\n🏁 Snapshot de dimensões finalizado.")


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    main()
