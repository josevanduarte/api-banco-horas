
from flask import Flask, request, jsonify
import hashlib
import requests
from datetime import datetime

app = Flask(__name__)

TOKEN_ORIGINAL = "mRvd11QSxXs5LUL$CfW1"
USER = "02297349289"
API_URL = "https://stou.ifractal.com.br/i9saude/rest/"

def gerar_token_sha256(data_formatada):
    token_concatenado = TOKEN_ORIGINAL + data_formatada
    return hashlib.sha256(token_concatenado.encode()).hexdigest()

@app.route("/")
def home():
    return "✅ API Horas Extras está online! Use /consultar-horas-extras?inicio=...&fim=..."

@app.route("/consultar-horas-extras", methods=["GET"])
def consultar_horas_extras():
    dtde = request.args.get("inicio")
    dtate = request.args.get("fim")

    if not dtde or not dtate:
        return jsonify({"erro": "Parâmetros 'inicio' e 'fim' são obrigatórios. Ex: ?inicio=01/01/2025&fim=06/08/2025"}), 400

    data_hoje = datetime.now().strftime("%d/%m/%Y")
    token = gerar_token_sha256(data_hoje)

    headers = {
        "Content-Type": "application/json",
        "User": USER,
        "Token": token
    }

    body = {
        "pag": "ponto_relatorio_hora_extra",
        "cmd": "get",
        "dtde": dtde,
        "dtate": dtate,
       "alteracao": False
    }

    try:
        response = requests.post(API_URL, json=body, headers=headers)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
