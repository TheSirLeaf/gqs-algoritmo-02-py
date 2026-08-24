import json
import os

ARQUIVO_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "habitos.json")


def carregar_dados():
    padrao = {"proximo_id": 1, "habitos": []}
    if not os.path.exists(ARQUIVO_DADOS):
        return padrao
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (OSError, json.JSONDecodeError):
        return padrao
    dados.setdefault("proximo_id", 1)
    dados.setdefault("habitos", [])
    return dados


def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
