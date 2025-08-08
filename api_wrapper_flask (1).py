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
    return "✅ API Ponto Consolidado está online! Use /ponto_consolidado_banco ou /ponto_consolidado_banco?inicio=01/01/2025&fim=31/01/2025"

@app.route("/ponto_consolidado_banco", methods=["GET"])
def consultar_ponto_consolidado():
    # Parâmetros opcionais
    dtde = request.args.get("inicio")
    dtate = request.args.get("fim")
    
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    token = gerar_token_sha256(data_hoje)

    headers = {
        "Content-Type": "application/json",
        "User": USER,
        "Token": token
    }

    # Body básico conforme documentação
    body = {
        "pag": "ponto_consolidado_banco",
        "cmd": "get"
    }
    
    # Adiciona filtros se fornecidos
    if dtde and dtate:
        body["dtde"] = dtde
        body["dtate"] = dtate
        body["alteracao"] = False  # Padrão para filtros com data

    try:
        response = requests.post(API_URL, json=body, headers=headers)
        
        # Log para debug
        print(f"📤 Body enviado: {body}")
        print(f"📥 Resposta recebida: {response.status_code}")
        
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/debug", methods=["GET"])
def debug_endpoint():
    """Endpoint para testar diferentes combinações"""
    dtde = request.args.get("inicio")
    dtate = request.args.get("fim")
    
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    token = gerar_token_sha256(data_hoje)
    
    body = {
        "pag": "ponto_consolidado_banco",
        "cmd": "get"
    }
    
    if dtde and dtate:
        body["dtde"] = dtde
        body["dtate"] = dtate
        body["alteracao"] = False
    
    return jsonify({
        "info": "Debug - não faz chamada real para API",
        "body_que_seria_enviado": body,
        "headers_que_seriam_enviados": {
            "Content-Type": "application/json",
            "User": USER,
            "Token": token[:10] + "..."  # Token truncado por segurança
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
