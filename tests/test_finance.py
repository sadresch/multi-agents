import pytest
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent
from financial_advisor.agent import root_agent

@pytest.mark.asyncio
async def test_agent_initialization():
    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    
    content = UserContent(parts=[Part(text="Olá")])
    response_text = ""
    async for event in runner.run_async(
        user_id=session.user_id, session_id=session.id, new_message=content
    ):
        # Captura apenas se houver texto, tratando o NoneType
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response_text += part.text

    # Verifica se ele respondeu (pelo menos o "Olá" ou o início da apresentação)
    assert len(response_text) > 0
    # Valida se parte do seu disclaimer está lá (ajuste conforme o texto exato do seu prompt)
    assert "Aviso Importante" in response_text or "Investimentos" in response_text

@pytest.mark.asyncio
async def test_request_analysis_flow():
    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    
    content = UserContent(parts=[Part(text="Quero analisar a PETR4")])
    response_text = ""
    async for event in runner.run_async(
        user_id=session.user_id, session_id=session.id, new_message=content
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text: # Checagem de segurança para não somar None
                    response_text += part.text
            
    assert "PETR4" in response_text