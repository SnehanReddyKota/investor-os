from pydantic import BaseModel
from dataclasses import dataclass
from typing import Any, TypeVar, Callable


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    input_model: type
    handler: Callable[..., Any]

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")

        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolDefinition:
        try:
            return self._tools[name]
        except KeyError:
            raise KeyError(f"Tool not found: {name}")

    def get_all(self) -> list[ToolDefinition]:
        return list(self._tools.values())

    def execute(self, name: str, arguments: dict[str, Any]) -> Any:
        tool = self.get(name)

        request = tool.input_model.model_validate(arguments)

        return tool.handler(request)

    def get_definitions(self) -> list[ToolDefinition]:
        return list(self._tools.values())
    