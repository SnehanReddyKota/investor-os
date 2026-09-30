import pytest

from investor_os.tools.company import (
    CompanyProfileRequest,
    company_profile_tool,
)
from investor_os.tools.registry import ToolRegistry


def create_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(company_profile_tool)
    return registry


def test_execute_valid_tool():
    registry = create_registry()

    result = registry.execute(
        "get_company_profile",
        {"ticker": "AAPL"},
    )

    assert result.ticker == "AAPL"
    assert result.name == "Apple Inc."


def test_execute_unknown_tool():
    registry = create_registry()

    with pytest.raises(KeyError, match="Tool not found"):
        registry.execute(
            "unknown_tool",
            {},
        )


def test_execute_invalid_arguments():
    registry = create_registry()

    with pytest.raises(ValueError):
        registry.execute(
            "get_company_profile",
            {"ticker": 123},
        )


def test_duplicate_tool_registration():
    registry = ToolRegistry()

    registry.register(company_profile_tool)

    with pytest.raises(
        ValueError,
        match="Tool already registered",
    ):
        registry.register(company_profile_tool)