from datetime import UTC, datetime

import requests

from cartola_pipeline.config.settings import BUCKET_NAME, DIMENSION_ENDPOINTS
from cartola_pipeline.utils.s3_helpers import exists_prefix, save_json, timestamp_utc


def snapshot_ja_existe(endpoint_name, data_particao):
    return exists_prefix(BUCKET_NAME, f"{endpoint_name}/data={data_particao}/")


def salvar_json(endpoint_name, data_particao, payload):
    key = f"{endpoint_name}/data={data_particao}/extract_{timestamp_utc()}.json"
    save_json(BUCKET_NAME, key, payload)


def main():
    hoje = datetime.now(UTC).date()
    print(f"📅 Executando snapshot de dimensões para {hoje}")

    for nome, url in DIMENSION_ENDPOINTS.items():
        print(f"\n🔎 Processando endpoint: {nome}")

        if snapshot_ja_existe(nome, hoje):
            print(f"⚠️ Snapshot já existe para {nome} em {hoje}. Pulando.")
            continue

        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Erro ao consultar {nome}")
            print(response.text)
            continue

        salvar_json(nome, hoje, response.json())

    print("\n🏁 Snapshot de dimensões finalizado.")


if __name__ == "__main__":
    main()
