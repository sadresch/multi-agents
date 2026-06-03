# Quantum Finance Manager

O **Quantum Finance Manager** é uma solução multi-agente avançada, desenvolvida com o *ADK (Agent Development Kit)*, projetada para atuar como um copiloto de assessoria financeira no mercado brasileiro. O sistema orquestra subagentes especializados que, em conjunto, analisam ativos da B3, avaliam cenários macroeconômicos e geram recomendações de portfólio personalizadas para investidores.



## Estrutura dos Agentes

O sistema é composto por um orquestrador central e três subagentes especialistas, cada um com responsabilidades e ferramentas dedicadas:

### 1. Orquestrador Central (`quantum_finance_manager`)
Gerencia o fluxo conversacional, interpreta a intenção do usuário e delega as tarefas para os subagentes, mantendo a coesão do contexto.

### 2. Agente de Dados B3 (`b3_data_agent`)
Especialista em extração de dados técnicos e fundamentos de ativos listados na Bolsa do Brasil.
* **Ferramentas:**
    * `get_price`: Consulta a API `Bolsai` para obter cotações em tempo real.
    * `get_stock_fundamentals`: Extrai indicadores como P/L, P/VP, ROE e Market Cap.
    * `get_fii_data`: Analisa métricas de fundos imobiliários (DY mensal, vacância).
    * `search_b3_ticker`: Mapeia nomes de empresas para tickers (ex: "Petrobras" para "PETR4").
* **Fluxo:** Segue um rigoroso protocolo de busca, onde nunca estima valores, priorizando sempre a consulta via `X-API-Key` na API oficial.

### 3. Analista de Mercado (`market_analyst_agent`)
Focado na interpretação macroeconômica e educacional de produtos financeiros.
* **Ferramentas:**
    * `get_selic_rate` e `get_cdi_rate`: Integração direta com APIs do Banco Central (SGS/BCB) para dados de taxas de juros.
    * `search_financial_info`: Base de conhecimento estruturada para explicar produtos como CDB, LCI, LCA e Tesouro Direto.
* **Responsabilidade:** Contextualiza o cenário brasileiro, comparando investimentos com a taxa livre de risco.

### 4. Estrategista de Carteira (`lead_advisor_agent`)
O consultor financeiro que sintetiza a análise técnica e macro em um plano de ação.
* **Ferramentas:**
    * `assess_investor_profile`: Avalia o perfil de risco do usuário (Conservador, Moderado ou Arrojado) baseando-se em idade, horizonte de tempo e objetivos.
    * `generate_portfolio_allocation`: Constrói um portfólio detalhado, definindo percentuais de alocação por classe de ativos, com justificativas técnicas e orientações de rebalanceamento.

## Especificações Técnicas: Tools e Prompts

| Agente | Objetivo Principal | Diretriz do Prompt |
|-----------|--------|----------------|
| **Orquestrador** | Raciocínio e Delegação | Delegar tarefas ao agente especialista e manter a coesão.|
| **B3 Data** | Precisão Factual | Proibir alucinações; priorizar dados reais da API Bolsai.|
| **Market Analyst** | Contexto Macro | Explicar produtos via ótica da Selic/CDI com fontes oficiais.|
| **Lead Advisor** | Consultoria Financeira | Construir portfólios baseados no perfil de risco do investidor.|

## Configuração e Instalação

### Pré-requisitos
* **Python 3.10+**
* **uv** (Gerenciador de pacotes e dependências)

### Instalação

```bash
# Clone este repositório.
git clone <url-do-seu-repositorio>
cd <nome-da-pasta-do-projeto>

# Instale o pacote e as dependências.
uv sync
```
### Autenticação
O sistema utiliza variáveis de ambiente para segurança. Crie um arquivo `.env` na raiz do projeto: 

```bash
BOLSAI_API_KEY=sua_chave_de_api_aqui
GOOGLE_API_KEY=sua_chave_de_api_aqui
```
Certifique-se de que seu ambiente esteja devidamente autenticado para acessar as APIs necessárias:

```bash
# Autenticação de serviço
gcloud auth application-default login
gcloud auth application-default set-quota-project <seu-project-id>
```

## Execução
Para esse projeto foi utilizado a interação via CLI:

* Execução Local:

```bash
adk run quantum_finance_manager
```

## Exemplo de Raciocínio (Workflow)
Quando o usuário pergunta *"Onde devo investir R$ 50 mil sendo um investidor moderado?"*, o fluxo segue esta lógica:

* **Lead Advisor:** Identifica o perfil (Moderado) e chama assess_investor_profile.

* **Orquestrador:** Aciona o market_analyst para buscar o cenário atual (Selic/CDI).

* **Orquestrador:** Solicita ao b3_data_agent cotações e fundamentos.

* **Lead Advisor:** Gera a alocação com generate_portfolio_allocation.


## Aviso Legal (Disclaimer)
**Aviso Importante: Apenas para Fins Educacionais e Informativos.**
As recomendações de alocação e as análises apresentadas por este agente são geradas por um modelo de IA e não constituem consultoria financeira oficial, gestão de patrimônio ou recomendação de compra/venda de ativos.

Investimentos em renda variável e fundos imobiliários envolvem riscos inerentes. A rentabilidade passada não é garantia de resultados futuros. Recomendamos que o usuário realize sua própria diligência e consulte um assessor de investimentos certificado pela CVM antes de alocar capital.