from flask import Flask, request, jsonify
import hashlib
import requests
from datetime import datetime

app = Flask(__name__)

# Configurações da API
TOKEN_ORIGINAL = "123"        # Substituir pelo seu token original
USER = "User-login"           # Substituir pelo seu usuário
API_URL = "https://stou.ifractal.com.br/i9saude/rest/"

def gerar_token_sha256():
    """Gera o token SHA256 usando o token original + data atual."""
    data_atual = datetime.now().strftime("%d/%m/%Y")
    token_concat = f"{TOKEN_ORIGINAL}{data_atual}"
    return hashlib.sha256(token_concat.encode()).hexdigest()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "mensagem": "API está rodando no Render"})

@app.route("/consultar", methods=["GET"])
def consultar():
    try:
        # Gera token do dia
        token_dinamico = gerar_token_sha256()

        # Cabeçalho
        headers = {
            "Content-Type": "application/json",
            "User": USER,
            "Token": token_dinamico
        }

        # Base do payload
        payload = {
            "pag": "ponto_consolidado_banco",
            "cmd": "get"
        }

        # Lista de parâmetros aceitos pela API
        filtros_permitidos = [
            "tipo_operacao_em_lote", "dtde", "dtate", "apenas_extrato",
            "pendente_pagamento", "finalizados", "cod_pessoa", "centesimal",
            "cod_banco_horas", "cod_empresa", "cod_unidade", "cod_cargo",
            "demitido", "cod_centro_custo", "cod_hierarquia"
        ]

        # Adiciona filtros passados pela URL
        for filtro in filtros_permitidos:
            valor = request.args.get(filtro)
            if valor is not None:
                # Converte valores booleanos se necessário
                if valor.lower() in ["true", "false"]:
                    valor = valor.lower() == "true"
                # Converte inteiros
                elif valor.isdigit():
                    valor = int(valor)
                payload[filtro] = valor

        # Faz a requisição POST
        response = requests.post(API_URL, json=payload, headers=headers)

        # Retorna a resposta da API original
        return jsonify(response.json())

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
