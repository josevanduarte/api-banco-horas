from flask import Flask, request, jsonify
import hashlib
import requests
from datetime import datetime

app = Flask(__name__)

# CONFIGURAÇÕES FIXAS
TOKEN_ORIGINAL = "mRvd11QSxXs5LUL$CfW1"  # Substitua pelo seu token original
USER = "02297349289"                      # Substitua pelo seu usuário
API_URL = "https://stou.ifractal.com.br/i9saude/rest/"

def gerar_token_sha256(data_formatada):
    """Gera o token SHA256 usando o token original + data informada."""
    token_concatenado = TOKEN_ORIGINAL + data_formatada
    return hashlib.sha256(token_concatenado.encode()).hexdigest()

def get_headers():
    """Monta os headers com token dinâmico do dia."""
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    return {
        "Content-Type": "application/json",
        "User": USER,
        "Token": gerar_token_sha256(data_hoje)
    }

@app.route("/")
def home():
    return "✅ API Banco de Horas online! Use /banco_horas com filtros via query string."

@app.route("/banco_horas", methods=["GET"])
def banco_horas():
    """Consulta ponto_consolidado_banco com filtros opcionais via URL."""
    body = {
        "pag": "ponto_consolidado_banco",
        "cmd": "get"
    }

    # Adiciona todos os filtros passados via URL
    for key in request.args:
        valor = request.args.get(key)
        # Converte booleanos e inteiros automaticamente
        if valor.lower() in ["true", "false"]:
            valor = valor.lower() == "true"
        elif valor.isdigit():
            valor = int(valor)
        body[key] = valor

    try:
        response = requests.post(API_URL, json=body, headers=get_headers())
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
