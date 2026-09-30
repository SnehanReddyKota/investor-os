from google.genai import types

from investor_os.tools.registry import ToolDefinition


def to_gemini_tool_definition(
    tool: ToolDefinition,
) -> types.FunctionDeclaration:
    return types.FunctionDeclaration(
        name=tool.name,
        description=tool.description,
        parameters_json_schema=tool.input_model.model_json_schema(),
    )