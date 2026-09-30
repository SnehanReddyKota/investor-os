import json

from investor_os.domain.research import ResearchRequest, ResearchResponse
from investor_os.llm.client import LLMClient
from investor_os.llm.gemini_tools import to_gemini_tool_definition
from investor_os.tools.registry import ToolRegistry

class ResearchService:
    def __init__(self, llm_client: LLMClient, tool_registry: ToolRegistry):
        self._llm_client = llm_client
        self._tool_registry = tool_registry



    def research(self, request: ResearchRequest) -> ResearchResponse:

        tools = [
            to_gemini_tool_definition(tool)
            for tool in self._tool_registry.get_definitions()
        ]

        prompt = f"""
        Research the company identified by ticker {request.ticker}.

        User question:
        {request.question}

        Use the available company profile tool when appropriate.
        Return the final answer as the requested structured response.
        """

        # 1. Ask the LLM
        response = self._llm_client.generate_with_tools(
            prompt,
            tools,
        )

        # 2. Check whether Gemini requested a tool
        function_calls = response.function_calls

        if not function_calls:
            raise ValueError("LLM did not request a tool")

        function_call = function_calls[0]

        # 3. Extract tool request
        tool_name = function_call.name
        arguments = dict(function_call.args)

        # 4. Execute through the application-controlled registry
        tool_result = self._tool_registry.execute(
            tool_name,
            arguments,
        )

        # 5. Send tool result back to Gemini
        final_response = self._llm_client.generate_with_tool_result(
        prompt=prompt,
        original_response=response,
        function_call=function_call,
        tool_definitions=tools,
        tool_result=tool_result.model_dump(),
        )


        # 6. Convert final response to our domain model
        return ResearchResponse.model_validate_json(
        final_response.text
        )


    

    def _build_prompt(self, request: ResearchRequest) -> str:
        if request.question:
            return f"Research {request.ticker} : {request.question}"
        
        return f"Provide default research for {request.ticker}."