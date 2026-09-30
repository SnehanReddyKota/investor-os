import pytest

from investor_os.application.research_service import ResearchService
from investor_os.domain.research import ResearchRequest
from investor_os.llm.gemini import GeminiClient
from investor_os.tools.company import company_profile_tool
from investor_os.tools.market import market_summary_tool
from investor_os.tools.registry import ToolRegistry


class RecordingToolRegistry(ToolRegistry):
    def __init__(self):
        super().__init__()
        self.executed_tools = []

    def execute(self, name: str, arguments: dict):
        self.executed_tools.append(name)
        return super().execute(name, arguments)


@pytest.mark.integration
def test_research_service_executes_company_profile_tool():
    registry = RecordingToolRegistry()

    registry.register(company_profile_tool)
    registry.register(market_summary_tool)

    service = ResearchService(
        GeminiClient(),
        registry,
    )

    request = ResearchRequest(
        ticker="AAPL",
        question="What is the basic company profile?",
    )

    response = service.research(request)

    assert response.ticker == "AAPL"
    assert response.summary
    assert isinstance(response.key_points, list)

    assert registry.executed_tools
    assert registry.executed_tools[0] == "get_company_profile"


@pytest.mark.integration
def test_research_service_executes_market_summary_tool():
    registry = RecordingToolRegistry()

    registry.register(company_profile_tool)
    registry.register(market_summary_tool)

    service = ResearchService(
        GeminiClient(),
        registry,
    )

    request = ResearchRequest(
        ticker="AAPL",
        question="What is the current market summary and price?",
    )

    response = service.research(request)

    assert response.ticker == "AAPL"
    assert response.summary
    assert isinstance(response.key_points, list)

    assert registry.executed_tools
    assert registry.executed_tools[0] == "get_market_summary"