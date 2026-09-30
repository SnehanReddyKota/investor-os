from pydantic import BaseModel
from investor_os.tools.registry import ToolDefinition




class CompanyProfileRequest(BaseModel):
    ticker: str

class CompanyProfile(BaseModel):
    ticker: str
    name: str
    sector: str

def get_company_profile(request: CompanyProfileRequest) -> CompanyProfile:
    return CompanyProfile(
        ticker=request.ticker,
        name="Apple Inc.",
        sector="Technology",
    )

company_profile_tool = ToolDefinition(
    name="get_company_profile",
    description="Get basic company information for a ticker.",
    input_model=CompanyProfileRequest,
    handler=get_company_profile,
)

