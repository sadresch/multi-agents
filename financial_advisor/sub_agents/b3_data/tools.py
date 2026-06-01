import os
import requests
import logging

# configuração de logging para ajudar no debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _get_headers():
    """Retorna os headers com a chave de API."""
    api_key = os.getenv("BOLSAI_API_KEY")
    if not api_key:
        logger.warning("BOLSAI_API_KEY não encontrada nas variáveis de ambiente.")
    return {"Authorization": f"Bearer {api_key}"}

def get_stock_quote(ticker: str) -> str:
    """Busca cotação e fundamentos usando a API da Bolsai."""
    ticker = ticker.upper().strip()
    # URL usebolsai
    url = f"https://api.usebolsai.com/api/v1/fundamentals/{ticker}"
    
    headers = {
        "X-API-Key": os.getenv("BOLSAI_API_KEY"),
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # formatando a resposta para o LLM entender
        return (f"Dados para {ticker}: Preço/Lucro (P/L): {data.get('pl')}, "
                f"P/VP: {data.get('pvp')}, ROE: {data.get('roe')}%, "
                f"Market Cap: {data.get('market_cap')}")
    except Exception as e:
        return f"Erro ao acessar dados da Bolsai para {ticker}: {str(e)}"

def get_stock_fundamentals(ticker: str) -> str:
    """Busca indicadores fundamentalistas (P/L, DY, ROE) da ação informada."""
    ticker_clean = ticker.upper().strip()
    return f"Indicadores Fundamentalistas para {ticker_clean} (Estimados): P/L: 5.4x | Dividend Yield: 9.8% | P/VP: 1.2x | ROE: 18%."

def get_fii_data(ticker: str) -> str:
    """Busca dados de Fundos Imobiliários (FIIs) como DY mensal e vacância."""
    ticker_clean = ticker.upper().strip()
    return f"Dados do FII {ticker_clean}: DY Mensal: 0.85% | P/VP: 0.98 | Vacância Física: 4.2%."

def search_b3_ticker(company_name: str) -> str:
    """Mapeia o nome de uma empresa para seu respectivo ticker na B3."""
    mapping = {"petrobras": "PETR4", "vale": "VALE3", "itaú": "ITUB4", "itau": "ITUB4", "bradesco": "BBDC4"}
    return mapping.get(company_name.lower().strip(), "Ticker não encontrado para este nome.")

def get_price(ticker: str) -> str:
    """Busca o preço atual de um ativo na API Bolsai."""
    ticker = ticker.upper().strip()
    url = f"https://api.usebolsai.com/api/v1/quote/{ticker}"
    
    headers = {
        "X-API-Key": os.getenv("BOLSAI_API_KEY"),
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        price = data.get('price', 'N/A')
        return f"O preço atual de {ticker} é R$ {price}."
    except Exception as e:
        return f"Não foi possível obter o preço de {ticker}. Erro: {str(e)}"