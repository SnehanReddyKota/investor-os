from pydantic import BaseModel

from investor_os.tools.registry import ToolDefinition


class MarketSummaryRequest(BaseModel):
    ticker: str


class MarketSummary(BaseModel):
    ticker: str
    price: float



def get_market_summary(
    request: MarketSummaryRequest,
) -> MarketSummary:
    return MarketSummary(
        ticker=request.ticker,
        price=250.00,
    )

market_summary_tool = ToolDefinition(
    name="get_market_summary",
    description="Get current market summary and price for a ticker.",
    input_model=MarketSummaryRequest,
    handler=get_market_summary,
)