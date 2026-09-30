import pytest

from investor_os.application.research_service import ResearchService
from investor_os.domain.research import ResearchRequest
from investor_os.llm.gemini import GeminiClient
from investor_os.tools.registry import ToolRegistry
from investor_os.tools.company import company_profile_tool



@pytest.mark.integration
def test_gemini_research():

     # Arrange
    registry = ToolRegistry()
    registry.register(company_profile_tool)
    
    service = ResearchService(
        llm_client=GeminiClient(),
        tool_registry=registry,
    )
    
    request = ResearchRequest(
        ticker="AAPL",
        question="Give a short overview of Apple.",
    )

    response = service.research(request)

    assert response.ticker == "AAPL"
    assert response.summary
    assert isinstance(response.key_points, list)