from investor_os.llm.client import LLMClient
from typing import TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class MockFunctionCall:
    name = "get_company_profile"
    args = {"ticker": "AAPL"}


class MockToolResponse:
    function_calls = [MockFunctionCall()]


class MockFinalResponse:
    text = '{"ticker": "AAPL", "summary": "Mock research response", "key_points": []}'


class MockLLMClient(LLMClient):

    def generate(self, prompt: str) -> str:
        return '{"ticker": "AAPL", "summary": "Mock research response", "key_points": []}'

    def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
    ) -> T:
        return response_model(
            ticker="AAPL",
            summary="Mock research response",
            key_points=[],
        )

    def generate_with_tools(
        self,
        prompt: str,
        tools,
    ):
        return MockToolResponse()

    def generate_with_tool_result(
        self,
        prompt: str,
        original_response,
        function_call,
        tool_definitions,
        tool_result: dict,
    ):
        return MockFinalResponse()