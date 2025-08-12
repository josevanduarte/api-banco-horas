
from flask import Flask, request, jsonify
import hashlib
import requests
from datetime import datetime
import os

app = Flask(__name__)

# Configurações fixas
TOKEN_ORIGINAL = os.environ.get("IFRACTAL_TOKEN", "mRvd11QSxXs5LUL$CfW1")
USER = os.environ.get("IFRACTAL_USER", "02297349289")
API_URL = "https://stou.ifractal.com.br/i9saude/rest/"

def gerar_token_sha256(data_formatada):
    token_concatenado = TOKEN_ORIGINAL + data_formatada
    return hashlib.sha256(token_concatenado.encode("utf-8")).hexdigest()

@app.route("/ponto_banco_horas", methods=["GET"])
def ponto_banco_horas():
    # Captura parâmetros da URL
    dtde = request.args.get("dtde")
    dtate = request.args.get("dtate")
    cod_empresa = request.args.get("cod_empresa")
    cod_pessoa = request.args.get("cod_pessoa")

    # Data atual para o token
    data_atual = datetime.now().strftime("%d/%m/%Y")
    token_gerado = gerar_token_sha256(data_atual)

    headers = {
        "Content-Type": "application/json",
        "User": USER,
        "Token": token_gerado
    }

    body = {
        "pag": "ponto_consolidado_banco",
        "cmd": "get"
    }

    # Só adiciona filtros se vierem
    if dtde:
        body["dtde"] = dtde
    if dtate:
        body["dtate"] = dtate
    if cod_empresa:
        body["cod_empresa"] = int(cod_empresa)
    if cod_pessoa:
        body["cod_pessoa"] = int(cod_pessoa)

    # LOG no Render
    print("===== DEBUG REQUISIÇÃO IFRACTAL =====")
    print("HEADERS:", headers)
    print("BODY:", body)
    print("=====================================")

    try:
        resp = requests.post(API_URL, headers=headers, json=body, timeout=30)
        print("STATUS CODE:", resp.status_code)
        print("RESPOSTA BRUTA:", resp.text)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"error": True, "message": str(e)})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"info": "Use o endpoint /ponto_banco_horas com parametros dtde e dtate"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
