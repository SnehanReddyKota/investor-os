from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import TypeVar

T= TypeVar("T", bound=BaseModel)


class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        ...

    @abstractmethod
    def generate_structured(self,prompt: str, response_model: type[T]) -> T:
        ...

    @abstractmethod
    def generate_with_tool_result(
    self,
    prompt: str,
    original_response,
    function_call,
    tool_definitions,
    tool_result: dict,
    ):
        ...