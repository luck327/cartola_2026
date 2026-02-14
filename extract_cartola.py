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

    print(f"📦 Salvo em s3://{BUCKET_NAME}/{key}")


# =========================
# MAIN LOGIC
# =========================

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

    # Determinar última rodada consolidada
    if status_mercado == 1:  # mercado aberto
        rodada_max = rodada_atual - 1
    elif status_mercado == 2:  # mercado fechado
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

            # ---------------------------
            # PONTUADOS
            # ---------------------------
            url_pontuados = f"{ENDPOINT_PONTUADOS}/{rodada}"
            response_pontuados = requests.get(url_pontuados)

            if response_pontuados.status_code != 200:
                print(f"❌ Erro ao buscar pontuados da rodada {rodada}")
                print(response_pontuados.text)
                continue

            pontuados = response_pontuados.json()

            salvar_json(
                "atletas_pontuados",
                "rodada",
                rodada,
                pontuados
            )

            # ---------------------------
            # PARTIDAS
            # ---------------------------
            url_partidas = f"{ENDPOINT_PARTIDAS}/{rodada}"
            response_partidas = requests.get(url_partidas)

            if response_partidas.status_code != 200:
                print(f"❌ Erro ao buscar partidas da rodada {rodada}")
                print(response_partidas.text)
                continue

            partidas = response_partidas.json()

            salvar_json(
                "partidas",
                "rodada",
                rodada,
                partidas
            )

            # Atualiza controle após sucesso
            update_pipeline_state(rodada)

            print(f"✅ Rodada {rodada} processada com sucesso.")

    # Snapshot de mercado_status sempre
    salvar_json(
        "mercado_status",
        "data",
        datetime.utcnow().date(),
        status
    )

    print("\n🏁 Execução finalizada.")


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    main()
