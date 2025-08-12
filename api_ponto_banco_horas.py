
from flask import Flask, request, jsonify
import hashlib
import requests
from datetime import datetime

app = Flask(__name__)

# Configurações fixas
TOKEN_ORIGINAL = "mRvd11QSxXs5LUL$CfW1"
USER = "02297349289"
API_URL = "https://stou.ifractal.com.br/i9saude/rest/"

# Gera o token dinâmico com base na data atual
def gerar_token_sha256(data_formatada):
    token_concatenado = TOKEN_ORIGINAL + data_formatada
    return hashlib.sha256(token_concatenado.encode()).hexdigest()

def get_headers():
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    return {
        "Content-Type": "application/json",
        "User": USER,
        "Token": gerar_token_sha256(data_hoje)
    }

@app.route("/")
def home():
    return "✅ API Banco de Horas online! Use /ponto_consolidado_banco com parâmetros."

@app.route("/ponto_consolidado_banco", methods=["GET"])
def ponto_banco_horas():
    # Monta o corpo da requisição
    body = {
        "pag": "ponto_consolidado_banco",
        "cmd": "get"
    }

    # Adiciona filtros recebidos via query string (GET)
    for key in request.args:
        body[key] = request.args.get(key)

    try:
        response = requests.post(API_URL, json=body, headers=get_headers())
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
