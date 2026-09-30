import pytest

from investor_os.llm.gemini import GeminiClient
from investor_os.llm.gemini_tools import to_gemini_tool_definition
from investor_os.tools.company import (
    CompanyProfileRequest,
    get_company_profile,
)
from investor_os.tools.registry import ToolDefinition


@pytest.mark.integration
def test_gemini_requests_company_profile():
    tool = ToolDefinition(
        name="get_company_profile",
        description="Get basic company information for a ticker.",
        input_model=CompanyProfileRequest,
        handler=get_company_profile,
    )

    definition = to_gemini_tool_definition(tool)

    client = GeminiClient()

    response = client.generate_with_tools(
        "Get the company profile for Apple. Use the available tool.",
        [definition],
    )

    function_calls = response.function_calls

    assert function_calls
    assert function_calls[0].name == "get_company_profile"
    assert function_calls[0].args["ticker"] == "AAPL"