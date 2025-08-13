import requests
import hashlib
from datetime import datetime
import json
from typing import Optional, Dict, Any

class PontoBancoHorasAPI:
    """
    Cliente para acessar a API de Ponto Banco de Horas
    """
    
    def __init__(self, base_url: str, token_original: str, usuario: str):
        """
        Inicializa o cliente da API
        
        Args:
            base_url: URL base da API (ex: https://stou.ifractal.com.br/i9saude/rest/)
            token_original: Token original fornecido pela equipe de suporte
            usuario: Login do usuário
        """
        self.base_url = base_url.rstrip('/')
        self.token_original = token_original
        self.usuario = usuario
    
    def _gerar_token_criptografado(self) -> str:
        """
        Gera o token criptografado concatenando o token original com a data atual
        e aplicando hash SHA256
        
        Returns:
            Token criptografado em SHA256
        """
        data_atual = datetime.now().strftime("%d/%m/%Y")
        token_concatenado = self.token_original + data_atual
        
        # Criptografia SHA256
        token_criptografado = hashlib.sha256(token_concatenado.encode()).hexdigest()
        
        return token_criptografado
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Gera os headers necessários para a requisição
        
        Returns:
            Dicionário com os headers
        """
        return {
            "Content-Type": "application/json",
            "User": self.usuario,
            "Token": self._gerar_token_criptografado()
        }
    
    def consultar_extrato_banco_horas(self, 
                                    ate_data: Optional[str] = None,
                                    trazer_dados_ponto: Optional[bool] = None,
                                    centesimal: Optional[bool] = None,
                                    de_data: Optional[str] = None,
                                    cod_pessoa: Optional[int] = None,
                                    cod_banco_horas: Optional[int] = None,
                                    cod_empresa: Optional[int] = None,
                                    cod_unidade: Optional[int] = None,
                                    cod_cargo: Optional[int] = None,
                                    cod_funcao: Optional[str] = None,
                                    cod_centro_custo: Optional[int] = None,
                                    tipo_geracao: Optional[str] = None,
                                    apenas_feriado: Optional[bool] = None,
                                    demitidos: Optional[bool] = None) -> Dict[str, Any]:
        """
        Consulta o extrato do banco de horas
        
        Args:
            ate_data: Data final do período (formato: dd/mm/yyyy)
            trazer_dados_ponto: Se deve trazer dados do ponto
            centesimal: Se deve usar formato centesimal
            de_data: Data inicial do período (formato: dd/mm/yyyy)
            cod_pessoa: Código do funcionário
            cod_banco_horas: Código do banco de horas
            cod_empresa: Código da empresa
            cod_unidade: Código do departamento
            cod_cargo: Código do cargo
            cod_funcao: Código da função
            cod_centro_custo: Código do centro de custo
            tipo_geracao: Tipo de compensação
            apenas_feriado: Listar apenas dias de feriado
            demitidos: Incluir funcionários demitidos
        
        Returns:
            Resposta da API em formato JSON
        """
        
        # Corpo da requisição
        body = {
            "pag": "ponto_banco_horas_extrato",
            "cmd": "get"
        }
        
        # Adiciona filtros opcionais ao corpo da requisição
        if ate_data is not None:
            body["atedt"] = ate_data
        if trazer_dados_ponto is not None:
            body["trazer_dados_ponto"] = trazer_dados_ponto
        if centesimal is not None:
            body["centesimal"] = centesimal
        if de_data is not None:
            body["dedt"] = de_data
        if cod_pessoa is not None:
            body["cod_pessoa"] = cod_pessoa
        if cod_banco_horas is not None:
            body["cod_banco_horas"] = cod_banco_horas
        if cod_empresa is not None:
            body["cod_empresa"] = cod_empresa
        if cod_unidade is not None:
            body["cod_unidade"] = cod_unidade
        if cod_cargo is not None:
            body["cod_cargo"] = cod_cargo
        if cod_funcao is not None:
            body["cod_funcao"] = cod_funcao
        if cod_centro_custo is not None:
            body["cod_centro_custo"] = cod_centro_custo
        if tipo_geracao is not None:
            body["tipo_geracao"] = tipo_geracao
        if apenas_feriado is not None:
            body["apenas_feriado"] = apenas_feriado
        if demitidos is not None:
            body["demitidos"] = demitidos
        
        try:
            # Faz a requisição POST
            response = requests.post(
                self.base_url,
                headers=self._get_headers(),
                json=body,
                timeout=30
            )
            
            # Verifica se a requisição foi bem-sucedida
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return {"erro": str(e)}
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            return {"erro": f"Resposta inválida: {e}"}

def main():
    """
    Exemplo de uso da classe PontoBancoHorasAPI
    """
    
    # Configurações da API
    BASE_URL = "https://stou.ifractal.com.br/i9saude/rest/"
    TOKEN_ORIGINAL = "mRvd11QSxXs5LUL$CfW1"
    USUARIO = "02297349289"
    
    # Criar instância do cliente
    api_client = PontoBancoHorasAPI(BASE_URL, TOKEN_ORIGINAL, USUARIO)
    
    print("=== Cliente API Ponto Banco de Horas ===")
    print(f"Token criptografado: {api_client._gerar_token_criptografado()}")
    print()
    
    # Exemplo 1: Consulta simples
    print("1. Consultando extrato básico...")
    resultado = api_client.consultar_extrato_banco_horas()
    print(f"Resultado: {json.dumps(resultado, indent=2, ensure_ascii=False)}")
    print()
    
    # Exemplo 2: Consulta com filtros
    print("2. Consultando com filtros...")
    resultado_filtrado = api_client.consultar_extrato_banco_horas(
        de_data="01/08/2025",
        ate_data="31/08/2025",
        trazer_dados_ponto=True,
        centesimal=True,
        cod_empresa=1
    )
    print(f"Resultado filtrado: {json.dumps(resultado_filtrado, indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    main()
