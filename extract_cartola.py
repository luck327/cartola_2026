import json
import requests
import boto3
from datetime import datetime

# =========================
# CONFIG
# =========================

BUCKET_NAME = "cartola-raw"
CONTROL_KEY = "control/pipeline_state.json"

ENDPOINT_STATUS = "https://api.cartola.globo.com/mercado/status"
ENDPOINT_PONTUADOS = "https://api.cartola.globo.com/atletas/pontuados"
ENDPOINT_PARTIDAS = "https://api.cartola.globo.com/partidas"

s3 = boto3.client("s3")


# =========================
# UTIL FUNCTIONS
# =========================

def get_pipeline_state():
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=CONTROL_KEY)
        return json.loads(obj["Body"].read())
    except s3.exceptions.NoSuchKey:
        return {
            "ultima_rodada_processada": 0,
            "ultima_execucao": None
        }


def update_pipeline_state(nova_rodada):
    state = {
        "ultima_rodada_processada": nova_rodada,
        "ultima_execucao": datetime.utcnow().isoformat()
    }

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=CONTROL_KEY,
        Body=json.dumps(state, indent=2)
    )


def rodada_ja_existe(rodada):
    prefix = f"atletas_pontuados/rodada={rodada}/"
    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=prefix,
        MaxKeys=1
    )
    return "Contents" in response


def salvar_json(endpoint_name, particionador, valor_particao, payload):
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")

    key = (
        f"{endpoint_name}/"
        f"{particionador}={valor_particao}/"
        f"extract_{timestamp}.json"
    )

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps(payload)
    )

    print(f"Salvo em s3://{BUCKET_NAME}/{key}")


# =========================
# MAIN LOGIC
# =========================

def main():

    print("🔍 Lendo estado do pipeline...")
    state = get_pipeline_state()
    ultima_processada = state["ultima_rodada_processada"]

    print("📡 Consultando mercado/status...")
    status = requests.get(ENDPOINT_STATUS).json()

    rodada_consolidada = status.get("rodada_anterior")
    status_mercado = status.get("status_mercado")

    print(f"Rodada consolidada: {rodada_consolidada}")
    print(f"Última processada: {ultima_processada}")

    # Mercado fechado geralmente é status 2
    if rodada_consolidada is None:
        print("⚠️ Não foi possível identificar rodada.")
        return

    if rodada_consolidada <= ultima_processada:
        print("✅ Nenhuma nova rodada para processar.")
        return

    if rodada_ja_existe(rodada_consolidada):
        print("⚠️ Rodada já existe no S3. Abortando.")
        return

    print(f"🚀 Processando rodada {rodada_consolidada}...")

    # Extrair pontuados
    pontuados = requests.get(ENDPOINT_PONTUADOS).json()
    salvar_json(
        "atletas_pontuados",
        "rodada",
        rodada_consolidada,
        pontuados
    )

    # Extrair partidas
    partidas = requests.get(ENDPOINT_PARTIDAS).json()
    salvar_json(
        "partidas",
        "rodada",
        rodada_consolidada,
        partidas
    )

    # Salvar snapshot de status
    salvar_json(
        "mercado_status",
        "data",
        datetime.utcnow().date(),
        status
    )

    # Atualizar controle
    update_pipeline_state(rodada_consolidada)

    print("✅ Rodada processada com sucesso.")


if __name__ == "__main__":
    main()
