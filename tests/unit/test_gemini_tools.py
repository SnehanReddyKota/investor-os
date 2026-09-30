from google.genai import types

from investor_os.llm.gemini_tools import to_gemini_tool_definition
from investor_os.tools.company import (
    CompanyProfileRequest,
    get_company_profile,
)
from investor_os.tools.registry import ToolDefinition


def test_to_gemini_tool_definition():
    tool = ToolDefinition(
        name="get_company_profile",
        description="Get basic company information for a ticker.",
        input_model=CompanyProfileRequest,
        handler=get_company_profile,
    )

    definition = to_gemini_tool_definition(tool)

    assert isinstance(definition, types.FunctionDeclaration)
    assert definition.name == "get_company_profile"
    assert definition.description