from flask import Flask, request, jsonify
import hashlib
import requests
from datetime import datetime

app = Flask(__name__)

# Configurações da API externa
TOKEN_ORIGINAL = "mRvd11QSxXs5LUL$CfW1"  # Seu token original
USER = "02297349289"                      # Usuário fornecido pela API
API_URL = "https://stou.ifractal.com.br/i9saude/rest/"

# Função para gerar o token SHA256
def gerar_token_sha256(data_formatada):
    token_concatenado = TOKEN_ORIGINAL + data_formatada
    return hashlib.sha256(token_concatenado.encode()).hexdigest()

# Função para montar o header da requisição
def get_headers():
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    return {
        "Content-Type": "application/json",
        "User": USER,
        "Token": gerar_token_sha256(data_hoje)
    }

# Endpoint principal para o ponto banco de horas
@app.route("/ponto_banco_horas", methods=["GET"])
def ponto_banco_horas():
    # Monta o corpo base
    body = {
        "pag": "ponto_consolidado_banco",
        "cmd": "get"
    }
    # Adiciona todos os parâmetros passados via URL
    for key in request.args:
        body[key] = request.args.get(key)

    try:
        response = requests.post(API_URL, json=body, headers=get_headers())
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
