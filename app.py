from flask import Flask, request, jsonify
import hashlib
import requests
from datetime import datetime

app = Flask(__name__)

# CONFIGURAÇÕES FIXAS
TOKEN_ORIGINAL = "mRvd11QSxXs5LUL$CfW1"        # Substitua pelo token fornecido pelo suporte
USER = "02297349289"           # Substitua pelo seu login de usuário
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
    return "✅ API ponto_banco_horas_extrato online! Use /ponto_banco_horas_extrato com parâmetros via query string."

@app.route("/ponto_banco_horas_extrato", methods=["GET"])
def ponto_banco_horas_extrato():
    """Consulta o endpoint ponto_banco_horas_extrato com filtros opcionais via URL."""
    body = {
        "pag": "ponto_banco_horas_extrato",
        "cmd": "get"
    }

    # Lista de filtros permitidos conforme documentação
    filtros_permitidos = [
        "dtate", "trazer_dados_ponto", "centesimal", "dtde", "cod_pessoa",
        "cod_banco_horas", "cod_empresa", "cod_unidade", "cod_cargo", "cod_funcao",
        "cod_centro_custo", "tipo_geracao", "apenas_feriado", "demitidos"
    ]

    # Adiciona apenas filtros válidos que forem passados na URL
    for filtro in filtros_permitidos:
        valor = request.args.get(filtro)
        if valor is not None:
            if valor.lower() in ["true", "false"]:
                valor = valor.lower() == "true"
            elif valor.isdigit():
                valor = int(valor)
            body[filtro] = valor

    try:
        response = requests.post(API_URL, json=body, headers=get_headers())
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
