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

def converter_boolean(valor):
    """Converte string para boolean"""
    if isinstance(valor, str):
        return valor.lower() in ['true', '1', 'sim', 's']
    return bool(valor)

def converter_integer(valor):
    """Converte string para integer"""
    try:
        return int(valor) if valor else None
    except ValueError:
        return None

@app.route("/")
def home():
    return """
    ✅ API Ponto Consolidado está online!
    
    📋 Endpoint: GET /ponto_consolidado_banco
    
    🔧 Filtros disponíveis:
    • tipo_operacao_em_lote (string)
    • dtde (date) - formato: DD/MM/YYYY
    • dtate (date) - formato: DD/MM/YYYY
    • apenas_extrato (boolean)
    • pendente_pagamento (boolean)
    • finalizados (boolean)
    • cod_pessoa (integer)
    • centesimal (boolean)
    • cod_banco_horas (integer)
    • cod_empresa (integer)
    • cod_unidade (integer)
    • cod_cargo (integer)
    • demitido (boolean)
    • cod_centro_custo (integer)
    • cod_hierarquia (integer)
    
    📝 Exemplo: /ponto_consolidado_banco?dtde=01/07/2025&dtate=06/08/2025&apenas_extrato=true
    """

@app.route("/ponto_consolidado_banco", methods=["GET"])
def consultar_ponto_consolidado():
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    token = gerar_token_sha256(data_hoje)

    headers = {
        "Content-Type": "application/json",
        "User": USER,
        "Token": token
    }

    # Body básico obrigatório
    body = {
        "pag": "ponto_consolidado_banco",
        "cmd": "get"
    }
    
    # Campos de filtro opcionais
    filtros = {}
    
    # String
    if request.args.get("tipo_operacao_em_lote"):
        filtros["tipo_operacao_em_lote"] = request.args.get("tipo_operacao_em_lote")
    
    # Datas
    if request.args.get("dtde"):
        filtros["dtde"] = request.args.get("dtde")
    if request.args.get("dtate"):
        filtros["dtate"] = request.args.get("dtate")
    
    # Booleans
    if request.args.get("apenas_extrato") is not None:
        filtros["apenas_extrato"] = converter_boolean(request.args.get("apenas_extrato"))
    if request.args.get("pendente_pagamento") is not None:
        filtros["pendente_pagamento"] = converter_boolean(request.args.get("pendente_pagamento"))
    if request.args.get("finalizados") is not None:
        filtros["finalizados"] = converter_boolean(request.args.get("finalizados"))
    if request.args.get("centesimal") is not None:
        filtros["centesimal"] = converter_boolean(request.args.get("centesimal"))
    if request.args.get("demitido") is not None:
        filtros["demitido"] = converter_boolean(request.args.get("demitido"))
    
    # Integers
    if request.args.get("cod_pessoa"):
        cod_pessoa = converter_integer(request.args.get("cod_pessoa"))
        if cod_pessoa is not None:
            filtros["cod_pessoa"] = cod_pessoa
    
    if request.args.get("cod_banco_horas"):
        cod_banco_horas = converter_integer(request.args.get("cod_banco_horas"))
        if cod_banco_horas is not None:
            filtros["cod_banco_horas"] = cod_banco_horas
    
    if request.args.get("cod_empresa"):
        cod_empresa = converter_integer(request.args.get("cod_empresa"))
        if cod_empresa is not None:
            filtros["cod_empresa"] = cod_empresa
    
    if request.args.get("cod_unidade"):
        cod_unidade = converter_integer(request.args.get("cod_unidade"))
        if cod_unidade is not None:
            filtros["cod_unidade"] = cod_unidade
    
    if request.args.get("cod_cargo"):
        cod_cargo = converter_integer(request.args.get("cod_cargo"))
        if cod_cargo is not None:
            filtros["cod_cargo"] = cod_cargo
    
    if request.args.get("cod_centro_custo"):
        cod_centro_custo = converter_integer(request.args.get("cod_centro_custo"))
        if cod_centro_custo is not None:
            filtros["cod_centro_custo"] = cod_centro_custo
    
    if request.args.get("cod_hierarquia"):
        cod_hierarquia = converter_integer(request.args.get("cod_hierarquia"))
        if cod_hierarquia is not None:
            filtros["cod_hierarquia"] = cod_hierarquia
    
    # Adiciona filtros ao body se existirem
    if filtros:
        body.update(filtros)

    try:
        response = requests.post(API_URL, json=body, headers=headers)
        
        # Log para debug
        print(f"📤 Body enviado: {body}")
        print(f"📥 Status da resposta: {response.status_code}")
        
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/debug", methods=["GET"])
def debug_endpoint():
    """Endpoint para visualizar o body que seria enviado"""
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    token = gerar_token_sha256(data_hoje)
    
    # Processa todos os parâmetros da mesma forma que o endpoint principal
    body = {"pag": "ponto_consolidado_banco", "cmd": "get"}
    filtros = {}
    
    # Processa todos os filtros (mesmo código do endpoint principal)
    if request.args.get("tipo_operacao_em_lote"):
        filtros["tipo_operacao_em_lote"] = request.args.get("tipo_operacao_em_lote")
    
    if request.args.get("dtde"):
        filtros["dtde"] = request.args.get("dtde")
    if request.args.get("dtate"):
        filtros["dtate"] = request.args.get("dtate")
    
    if request.args.get("apenas_extrato") is not None:
        filtros["apenas_extrato"] = converter_boolean(request.args.get("apenas_extrato"))
    if request.args.get("pendente_pagamento") is not None:
        filtros["pendente_pagamento"] = converter_boolean(request.args.get("pendente_pagamento"))
    if request.args.get("finalizados") is not None:
        filtros["finalizados"] = converter_boolean(request.args.get("finalizados"))
    if request.args.get("centesimal") is not None:
        filtros["centesimal"] = converter_boolean(request.args.get("centesimal"))
    if request.args.get("demitido") is not None:
        filtros["demitido"] = converter_boolean(request.args.get("demitido"))
    
    # Integers
    for campo in ["cod_pessoa", "cod_banco_horas", "cod_empresa", "cod_unidade", 
                  "cod_cargo", "cod_centro_custo", "cod_hierarquia"]:
        if request.args.get(campo):
            valor = converter_integer(request.args.get(campo))
            if valor is not None:
                filtros[campo] = valor
    
    if filtros:
        body.update(filtros)
    
    return jsonify({
        "info": "🐛 DEBUG - Não faz chamada real para API",
        "parametros_recebidos": dict(request.args),
        "body_que_seria_enviado": body,
        "total_filtros_aplicados": len(filtros),
        "token_gerado": f"{token[:10]}..." # Token truncado por segurança
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
