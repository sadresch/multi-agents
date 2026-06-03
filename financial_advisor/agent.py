from dotenv import load_dotenv
load_dotenv()

from . import prompt
from google.adk.agents import LlmAgent

# funções dos subagentes
from .sub_agents.b3_data.tools import get_stock_quote, get_stock_fundamentals, get_fii_data, search_b3_ticker, get_price
from .sub_agents.data_analyst.tools import get_selic_rate, get_cdi_rate
from .sub_agents.lead_advisor.tools import assess_investor_profile, generate_portfolio_allocation

# orquestrador Central
root_agent = LlmAgent(
    name="quantum_finance_manager",
    model="gemini-3.5-flash",
    instruction=prompt.QUANTUM_FINANCE_MANAGER_PROMPT,
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

if __name__ == "__main__":
    print("--- Quantum Finance Manager Iniciado ---")
    print("--- Digite sua pergunta sobre o mercado ou 'sair' para encerrar ---")
    
    while True:
        try:
            user_input = input("\nVocê: ")
            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("Encerrando o agente. Até logo!")
                break
            
            # Chama o agente para processar pergunta
            resposta = root_agent.run(user_input)
            print(f"Agente: {resposta}")
            
        except Exception as e:
            print(f"Erro ao processar: {e}")