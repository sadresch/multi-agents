"""
Ferramentas do Lead Advisor para geração de recomendações de portfólio.
"""

from typing import Optional, List, Any


def assess_investor_profile(
    idade: int,
    objetivo: str,
    horizonte_anos: int,
    tolerancia_risco: str,
    valor_investimento: float,
    renda_mensal: Optional[float] = None,
    tem_reserva_emergencia: bool = False,
) -> dict:
    """
    Avalia o perfil do investidor e classifica como Conservador, Moderado ou Arrojado.

    Args:
        idade: Idade do investidor.
        objetivo: Objetivo financeiro (aposentadoria, casa própria, renda extra, etc.).
        horizonte_anos: Prazo de investimento em anos.
        tolerancia_risco: Auto-declarado: 'baixo', 'medio' ou 'alto'.
        valor_investimento: Valor disponível para investir em R$.
        renda_mensal: Renda mensal em R$ (opcional).
        tem_reserva_emergencia: Se já possui reserva de emergência.

    Returns:
        Perfil calculado, alocação sugerida por classe de ativo e observações.
    """
    score = 0

    # Pontuação por horizonte de tempo
    if horizonte_anos >= 10:
        score += 3
    elif horizonte_anos >= 5:
        score += 2
    elif horizonte_anos >= 2:
        score += 1

    # Pontuação por tolerância declarada
    risco_map = {"baixo": 0, "medio": 2, "alto": 4}
    score += risco_map.get(tolerancia_risco.lower(), 1)

    # Pontuação por idade (inversamente proporcional)
    if idade < 30:
        score += 3
    elif idade < 45:
        score += 2
    elif idade < 60:
        score += 1

    # Bônus: tem reserva de emergência
    if tem_reserva_emergencia:
        score += 1

    # Determinação do perfil
    if score <= 4:
        perfil = "Conservador"
        alocacao = {
            "Renda Fixa (CDB/LCI/LCA)": "50%",
            "Tesouro Direto": "30%",
            "FIIs": "10%",
            "Renda Variável (Ações)": "5%",
            "Reserva de Liquidez (Tesouro Selic)": "5%",
        }
        descricao = "Prioriza segurança e preservação de capital. Aceita rentabilidade menor para evitar perdas."

    elif score <= 7:
        perfil = "Moderado"
        alocacao = {
            "Renda Fixa (CDB/LCI/LCA)": "30%",
            "Tesouro Direto (IPCA+)": "20%",
            "FIIs": "20%",
            "Renda Variável (Ações)": "20%",
            "Reserva de Liquidez (Tesouro Selic)": "10%",
        }
        descricao = "Equilibra segurança e crescimento. Aceita volatilidade moderada para rentabilidade superior ao CDI."

    else:
        perfil = "Arrojado"
        alocacao = {
            "Renda Variável (Ações)": "40%",
            "FIIs": "20%",
            "Renda Fixa (IPCA+/Pré)": "15%",
            "ETFs / BDRs Internacionais": "15%",
            "Reserva de Liquidez (Tesouro Selic)": "10%",
        }
        descricao = "Busca máximo crescimento no longo prazo. Aceita oscilações relevantes na carteira."

    observacoes = []
    if not tem_reserva_emergencia:
        observacoes.append(
            "⚠️ PRIORITÁRIO: Constitua uma reserva de emergência (6-12x sua renda mensal) "
            "em Tesouro Selic ou CDB com liquidez diária ANTES de investir."
        )
    if idade > 55 and perfil == "Arrojado":
        observacoes.append(
            "⚠️ Atenção: perfil arrojado próximo da aposentadoria exige cuidado. "
            "Considere reduzir gradualmente a exposição a risco variável."
        )

    return {
        "perfil": perfil,
        "score": score,
        "descricao": descricao,
        "alocacao_sugerida": alocacao,
        "observacoes": observacoes,
        "valor_por_classe": {
            k: f"R$ {valor_investimento * float(v.strip('%')) / 100:,.2f}"
            for k, v in alocacao.items()
        },
    }


def generate_portfolio_allocation(
    perfil: str,
    valor_total: float,
    ativos_b3: Optional[List[str]] = None,
    objetivos_especificos: Optional[str] = None,
) -> dict:
    """
    Gera uma alocação de portfólio detalhada com produtos específicos.

    Args:
        perfil: 'Conservador', 'Moderado' ou 'Arrojado'.
        valor_total: Valor total disponível para investimento em R$.
        ativos_b3: Lista de ativos da B3 já analisados pelo b3_data_agent.
        objetivos_especificos: Objetivos adicionais (ex: 'dividendos mensais', 'valorização').

    Returns:
        Portfólio detalhado com produtos, valores, prazos e justificativas.
    """
    portfolios = {
        "Conservador": {
            "resumo": "Carteira defensiva com foco em preservação de capital e liquidez.",
            "meta_rentabilidade": "CDI + 1% a 2% ao ano",
            "produtos": [
                {
                    "produto": "Tesouro Selic 2027",
                    "classe": "Renda Fixa Pública",
                    "percentual": 25,
                    "valor": valor_total * 0.25,
                    "justificativa": "Liquidez diária, segurança máxima, acompanha SELIC",
                },
                {
                    "produto": "CDB 110% CDI (banco sólido)",
                    "classe": "Renda Fixa Privada",
                    "percentual": 30,
                    "valor": valor_total * 0.30,
                    "justificativa": "Rentabilidade acima do CDI com proteção do FGC",
                },
                {
                    "produto": "LCI/LCA Isento",
                    "classe": "Renda Fixa Isenta",
                    "percentual": 25,
                    "valor": valor_total * 0.25,
                    "justificativa": "Isenção de IR melhora rentabilidade líquida",
                },
                {
                    "produto": "Tesouro IPCA+ 2029",
                    "classe": "Renda Fixa Indexada",
                    "percentual": 10,
                    "valor": valor_total * 0.10,
                    "justificativa": "Proteção contra inflação no médio prazo",
                },
                {
                    "produto": "FII Papel (MXRF11 ou similar)",
                    "classe": "Fundos Imobiliários",
                    "percentual": 10,
                    "valor": valor_total * 0.10,
                    "justificativa": "Renda mensal isenta de IR, baixa volatilidade",
                },
            ],
        },
        "Moderado": {
            "resumo": "Carteira balanceada entre segurança e crescimento.",
            "meta_rentabilidade": "IPCA + 4% a 6% ao ano",
            "produtos": [
                {
                    "produto": "Tesouro IPCA+ 2035",
                    "classe": "Renda Fixa Indexada",
                    "percentual": 20,
                    "valor": valor_total * 0.20,
                    "justificativa": "Proteção da inflação + juros reais no longo prazo",
                },
                {
                    "produto": "CDB IPCA+ bancário",
                    "classe": "Renda Fixa Privada",
                    "percentual": 15,
                    "valor": valor_total * 0.15,
                    "justificativa": "Diversificação dentro da renda fixa com FGC",
                },
                {
                    "produto": "FIIs Diversificados (Tijolo + Papel)",
                    "classe": "Fundos Imobiliários",
                    "percentual": 20,
                    "valor": valor_total * 0.20,
                    "justificativa": "Renda passiva mensal + potencial de valorização",
                },
                {
                    "produto": "Ações Blue Chips (VALE3, ITUB4, PETR4)",
                    "classe": "Renda Variável",
                    "percentual": 25,
                    "valor": valor_total * 0.25,
                    "justificativa": "Empresas sólidas com bons dividendos e liquidez",
                },
                {
                    "produto": "ETF BOVA11 (Índice Ibovespa)",
                    "classe": "ETF",
                    "percentual": 10,
                    "valor": valor_total * 0.10,
                    "justificativa": "Diversificação automática nas maiores empresas da B3",
                },
                {
                    "produto": "Tesouro Selic (reserva)",
                    "classe": "Reserva de Liquidez",
                    "percentual": 10,
                    "valor": valor_total * 0.10,
                    "justificativa": "Liquidez para oportunidades e emergências",
                },
            ],
        },
        "Arrojado": {
            "resumo": "Carteira growth com foco em valorização de capital no longo prazo.",
            "meta_rentabilidade": "Ibovespa + 3% a 5% ao ano",
            "produtos": [
                {
                    "produto": "Ações Small Caps e Mid Caps",
                    "classe": "Renda Variável",
                    "percentual": 30,
                    "valor": valor_total * 0.30,
                    "justificativa": "Maior potencial de crescimento, aceita volatilidade",
                },
                {
                    "produto": "Ações Blue Chips dividendeiras",
                    "classe": "Renda Variável",
                    "percentual": 20,
                    "valor": valor_total * 0.20,
                    "justificativa": "Âncora da carteira com empresas sólidas",
                },
                {
                    "produto": "BDRs / ETFs Internacionais (IVVB11)",
                    "classe": "Diversificação Internacional",
                    "percentual": 15,
                    "valor": valor_total * 0.15,
                    "justificativa": "Exposição a dólar e mercado americano (S&P 500)",
                },
                {
                    "produto": "FIIs Tijolo (Logística e Lajes)",
                    "classe": "Fundos Imobiliários",
                    "percentual": 15,
                    "valor": valor_total * 0.15,
                    "justificativa": "Renda passiva mensal isenta de IR",
                },
                {
                    "produto": "Tesouro IPCA+ 2045",
                    "classe": "Renda Fixa",
                    "percentual": 10,
                    "valor": valor_total * 0.10,
                    "justificativa": "Diversificação e proteção da inflação no longo prazo",
                },
                {
                    "produto": "Tesouro Selic (reserva tática)",
                    "classe": "Reserva de Liquidez",
                    "percentual": 10,
                    "valor": valor_total * 0.10,
                    "justificativa": "Capital para aproveitar oportunidades de compra",
                },
            ],
        },
    }

    portfolio = portfolios.get(perfil, portfolios["Moderado"])

    # Incorporar ativos específicos analisados pelo b3_data_agent
    if ativos_b3:
        portfolio["ativos_analisados"] = ativos_b3

    # Adicionar metas e objetivos específicos
    if objetivos_especificos:
        portfolio["observacao_objetivos"] = (
            f"Considerando seu objetivo específico de '{objetivos_especificos}', "
            "a alocação foi orientada para maximizar esse resultado."
        )

    portfolio["disclaimer"] = (
        "⚠️ DISCLAIMER: Esta análise é gerada por sistema de IA da Quantum Finance "
        "e tem caráter informativo e educacional. Não constitui oferta ou recomendação "
        "formal de investimento. Consulte um assessor de investimentos certificado (CFP/CGA) "
        "registrado na CVM antes de tomar decisões financeiras. Rentabilidade passada "
        "não garante rentabilidade futura."
    )

    return portfolio