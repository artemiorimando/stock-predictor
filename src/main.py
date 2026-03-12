"""
Stock Price Predictor API

FastAPI service for time series stock price forecasting using Facebook Prophet.
Supports training on historical data from Yahoo Finance and serving predictions
via a REST endpoint.
"""

from fastapi import FastAPI, HTTPException

from schemas import StockInput, StockOutput
from model import predict, convert

app = FastAPI(
    title="Stock Price Predictor",
    description="Time series stock price forecasting powered by Facebook Prophet",
    version="1.0.0",
)


@app.post("/predict", response_model=StockOutput, status_code=200)
def get_prediction(payload: StockInput) -> StockOutput:
    """Forecast stock prices for the given ticker and horizon."""
    prediction_list = predict(payload.ticker, payload.days)

    if not prediction_list:
        raise HTTPException(
            status_code=400,
            detail=f"No trained model found for ticker '{payload.ticker}'. Train the model first.",
        )

    return StockOutput(
        ticker=payload.ticker,
        days=payload.days,
        forecast=convert(prediction_list),
    )
