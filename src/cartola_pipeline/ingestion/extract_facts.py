import json
from datetime import datetime

import requests

from cartola_pipeline.config.settings import (
    BUCKET_NAME,
    CONTROL_KEY,
    ENDPOINT_PARTIDAS,
    ENDPOINT_PONTUADOS,
    ENDPOINT_STATUS,
)
from cartola_pipeline.utils.s3_helpers import exists_prefix, s3, save_json, timestamp_utc


def get_pipeline_state():
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=CONTROL_KEY)
        return json.loads(obj["Body"].read())
    except s3.exceptions.NoSuchKey:
        return {
            "ultima_rodada_processada": 0,
            "ultima_execucao": None,
        }


def update_pipeline_state(nova_rodada):
    state = {
        "ultima_rodada_processada": nova_rodada,
        "ultima_execucao": datetime.utcnow().isoformat(),
    }
    s3.put_object(Bucket=BUCKET_NAME, Key=CONTROL_KEY, Body=json.dumps(state, indent=2))


def rodada_ja_existe(rodada):
    prefix = f"atletas_pontuados/rodada={rodada}/"
    return exists_prefix(BUCKET_NAME, prefix)


def salvar_json(endpoint_name, particionador, valor_particao, payload):
    key = (
        f"{endpoint_name}/"
        f"{particionador}={valor_particao}/"
        f"extract_{timestamp_utc()}.json"
    )
    save_json(BUCKET_NAME, key, payload)


def main():
    print("🔍 Lendo estado do pipeline...")
    state = get_pipeline_state()
    ultima_processada = state["ultima_rodada_processada"]

    print("📡 Consultando mercado/status...")
    status_response = requests.get(ENDPOINT_STATUS)
    if status_response.status_code != 200:
        print("❌ Erro ao consultar mercado/status")
        print(status_response.text)
        return

    status = status_response.json()
    rodada_atual = status.get("rodada_atual")
    status_mercado = status.get("status_mercado")

    if rodada_atual is None:
        print("⚠️ Não foi possível identificar rodada.")
        return

    if status_mercado == 1:
        rodada_max = rodada_atual - 1
    elif status_mercado == 2:
        rodada_max = rodada_atual
    else:
        print("⚠️ Status de mercado inesperado.")
        return

    print(f"Rodada máxima consolidada: {rodada_max}")
    print(f"Última rodada processada: {ultima_processada}")

    if rodada_max <= ultima_processada:
        print("✅ Nenhuma nova rodada para processar.")
    else:
        for rodada in range(ultima_processada + 1, rodada_max + 1):
            print(f"\n🚀 Processando rodada {rodada}...")

            if rodada_ja_existe(rodada):
                print(f"⚠️ Rodada {rodada} já existe no S3. Pulando.")
                continue

            response_pontuados = requests.get(f"{ENDPOINT_PONTUADOS}/{rodada}")
            if response_pontuados.status_code != 200:
                print(f"❌ Erro ao buscar pontuados da rodada {rodada}")
                print(response_pontuados.text)
                continue
            salvar_json("atletas_pontuados", "rodada", rodada, response_pontuados.json())

            response_partidas = requests.get(f"{ENDPOINT_PARTIDAS}/{rodada}")
            if response_partidas.status_code != 200:
                print(f"❌ Erro ao buscar partidas da rodada {rodada}")
                print(response_partidas.text)
                continue
            salvar_json("partidas", "rodada", rodada, response_partidas.json())

            update_pipeline_state(rodada)
            print(f"✅ Rodada {rodada} processada com sucesso.")

    salvar_json("mercado_status", "data", datetime.utcnow().date(), status)
    print("\n🏁 Execução finalizada.")


if __name__ == "__main__":
    main()
