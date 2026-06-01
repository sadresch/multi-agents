import requests

def get_selic_rate() -> str:
    """Busca a taxa SELIC atual via API do Banco Central do Brasil."""
    try:
        # Série 432: Taxa de juros - Selic acumulada no mês anualizada base 252 dias
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
        response = requests.get(url, timeout=10)
        data = response.json()
        return f"A taxa SELIC atual é {data[0]['valor']}% ao ano (Fonte: Banco Central)."
    except Exception as e:
        return "Não foi possível obter a taxa SELIC no momento."

def get_cdi_rate() -> str:
    """Busca a taxa CDI atual via API do Banco Central do Brasil."""
    try:
        # Série 12: Taxa de juros - CDI acumulada no mês
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados/ultimos/1?formato=json"
        response = requests.get(url, timeout=10)
        data = response.json()
        return f"A taxa CDI atual é {data[0]['valor']}% ao ano (Fonte: Banco Central)."
    except Exception as e:
        return "Não foi possível obter a taxa CDI no momento."

def search_financial_info(query: str) -> str:
    """
    Explica produtos financeiros. Para algo mais profundo, 
    podemos conectar a uma API de busca (como a API do Google ou Bing).
    """
    knowledge_base = {
        "CDB": "Certificado de Depósito Bancário: Título de renda fixa privado emitido por bancos.",
        "LCI": "Letra de Crédito Imobiliário: Isenta de IR, lastreada em financiamentos imobiliários.",
        "TESOURO": "Títulos públicos federais: Emissão do Tesouro Nacional, mais seguros do país."
    }
    
    query_upper = query.upper()
    for key, description in knowledge_base.items():
        if key in query_upper:
            return f"Informação sobre {key}: {description}"
            
    return f"Sobre '{query}': Produto financeiro regulado pela CVM/Bacen. Recomendo consultar o portal oficial da B3 ou Tesouro Direto para detalhes técnicos."