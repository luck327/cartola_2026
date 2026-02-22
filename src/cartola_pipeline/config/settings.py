"""Centralized project settings."""

BUCKET_NAME = "cartola-raw"
CONTROL_KEY = "control/pipeline_state.json"

ENDPOINT_STATUS = "https://api.cartola.globo.com/mercado/status"
ENDPOINT_PONTUADOS = "https://api.cartola.globo.com/atletas/pontuados"
ENDPOINT_PARTIDAS = "https://api.cartola.globo.com/partidas"

DIMENSION_ENDPOINTS = {
    "clubes": "https://api.cartola.globo.com/clubes",
    "posicoes": "https://api.cartola.globo.com/posicoes",
    "atletas_mercado": "https://api.cartola.globo.com/atletas/mercado",
    "rodadas": "https://api.cartola.globo.com/rodadas",
}
