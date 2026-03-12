"""Request and response schemas for the Stock Price Predictor API."""

from pydantic import BaseModel, Field


class StockInput(BaseModel):
    """Input schema: stock ticker and forecast horizon."""

    ticker: str = Field(..., description="Stock ticker symbol (e.g., MSFT, AAPL, GOOG)")
    days: int = Field(default=7, ge=1, le=365, description="Number of days to forecast")


class StockOutput(BaseModel):
    """Output schema: input parameters plus forecast data."""

    ticker: str
    days: int
    forecast: dict[str, float] = Field(..., description="Date → predicted trend value")
