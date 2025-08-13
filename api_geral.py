from flask import Flask, request, jsonify
import hashlib
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

TOKEN_ORIGINAL = "mRvd11QSxXs5LUL$CfW1"
USER = "02297349289"
API_URL = "https://stou.ifractal.com.br/i9saude/rest/"

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

@app.route("/ponto_banco_horas_extrato", methods=["GET"])
def ponto_banco_horas_extrato():
    # Obtém a data inicial da query string
    dtde = request.args.get("inicio")
    if not dtde:
        return jsonify({"erro": "Parâmetro 'inicio' é obrigatório."}), 400

    try:
        # Converte a data inicial para o formato datetime
        data_inicial = datetime.strptime(dtde, "%d/%m/%Y")
    except ValueError:
        return jsonify({"erro": "Formato de data inválido. Use 'dd/mm/aaaa'."}), 400

    # Calcula a data final (30 dias após a data inicial)
    data_final = data_inicial + timedelta(days=30)
    dtate = data_final.strftime("%d/%m/%Y")

    # Monta o corpo da requisição
    body = {
        "pag": "ponto_banco_horas_extrato",
        "cmd": "get",
        "dtde": dtde,
        "dtate": dtate
    }

    # Adiciona filtros adicionais da URL, se existirem
    for key in request.args:
        if key not in ["inicio"]:
            val = request.args.get(key)
            # Converte para booleano ou inteiro, se aplicável
            if val.lower() == "true":
                val = True
            elif val.lower() == "false":
                val = False
            elif val.isdigit():
                val = int(val)
            body[key] = val

    try:
        response = requests.post(API_URL, json=body, headers=get_headers())
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
