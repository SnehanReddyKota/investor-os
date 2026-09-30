from google import genai


from investor_os.domain.research import ResearchResponse
from investor_os.llm.client import LLMClient,T
from investor_os.config import get_gemini_api_key
from google.genai import types



class GeminiClient(LLMClient):
    def __init__(self):
        self.client = genai.Client(api_key=get_gemini_api_key())


    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )
        return response.text


    def generate_structured(self, prompt: str, response_model: type[T]) -> T:
        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": response_model,
            },
        )
        return response_model.model_validate_json(response.text)


    def generate_with_tools(
    self,
    prompt: str,
    tools: list[types.FunctionDeclaration],
    ):
        response = self.client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(function_declarations=tools)],
        ),
        )

        return response


    def generate_with_tool_result(
        self,
        prompt: str,
        original_response,
        function_call,
        tool_definitions,
        tool_result: dict,
    ):
        function_response_part = types.Part.from_function_response(
            name=function_call.name,
            response=tool_result,
        )

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part(text=prompt)
                ],
            ),
            original_response.candidates[0].content,
            types.Content(
                role="user",
                parts=[
                    function_response_part
                ],
            ),
        ]

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ResearchResponse,
            ),
        )

        return response

 