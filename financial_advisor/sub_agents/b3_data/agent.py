"""
Agente de Dados B3
Especialista em cotações e indicadores fundamentalistas da bolsa brasileira.
"""

from google.adk.agents import Agent
# .tools indicando que está no mesmo diretório
from .tools import (
    get_stock_quote,
    get_stock_fundamentals,
    get_fii_data,
    search_b3_ticker,
)

b3_data_agent = Agent(
    name="b3_data_agent",
    model="gemini-3.5-flash",
    description=(
        "Especialista em dados da B3 (Bolsa do Brasil). "
        "Fornece cotações em tempo real, indicadores fundamentalistas "
        "(P/L, P/VP, DY, ROE, EBITDA) e dados de FIIs."
    ),
    instruction="""
Você é o Agente de Dados B3 da Quantum Finance.

REGRA CRÍTICA: NUNCA invente ou estime cotações. 
Sempre use as ferramentas disponíveis para buscar dados reais.
Se a ferramenta retornar erro, informe claramente que os dados não estão disponíveis.

Suas responsabilidades:
1. Buscar cotações atualizadas de ações (ex: PETR4, VALE3, ITUB4).
2. Retornar indicadores fundamentalistas (P/L, P/VP, DY, ROE, Margem Líquida).
3. Para FIIs: P/VP, DY mensal, vacância, tipo de fundo.
4. Identificar o ticker correto quando o cliente mencionar o nome da empresa.

Fluxo obrigatório para qualquer ação mencionada:
1. Confirme o ticker com search_b3_ticker se necessário.
2. Busque a cotação com get_stock_quote.
3. Busque os fundamentais com get_stock_fundamentals.
4. Apresente os dados de forma organizada.
""",
    tools=[
        get_stock_quote, 
        get_stock_fundamentals, 
        get_fii_data, 
        search_b3_ticker
    ],
)