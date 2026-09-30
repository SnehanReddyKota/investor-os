from pydantic import BaseModel, field_validator


class ResearchRequest(BaseModel):
    ticker: str
    question: str | None = None

    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls, value: str) -> str:
        if not value.isalpha():
            raise ValueError("ticker must contain only letters")

        return value


    @field_validator("ticker", mode="before")
    @classmethod
    def normalize_ticker(cls, value) -> str:
        if isinstance(value, str):
            return value.strip().upper()
        
        return value

class ResearchResponse(BaseModel):
    ticker: str
    summary: str
    key_points: list[str]

    