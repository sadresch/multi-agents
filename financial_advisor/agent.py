from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import LlmAgent

# funções dos subagentes
from .sub_agents.b3_data.tools import get_stock_quote, get_stock_fundamentals, get_fii_data, search_b3_ticker, get_price
from .sub_agents.data_analyst.tools import get_selic_rate, get_cdi_rate
from .sub_agents.lead_advisor.tools import assess_investor_profile, generate_portfolio_allocation

# orquestrador Central
root_agent = LlmAgent(
    name="quantum_finance_manager",
    model="gemini-3.5-flash",
    instruction="""
    Você é o orquestrador principal da Quantum Finance. 
    ... (seu texto original) ...
    """,
    tools=[
        get_stock_quote, 
        get_price,
        get_stock_fundamentals, 
        get_fii_data, 
        search_b3_ticker,
        get_selic_rate, 
        get_cdi_rate,
        assess_investor_profile,
        generate_portfolio_allocation
    ]
)