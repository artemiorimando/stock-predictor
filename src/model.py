"""
Prophet-based stock price forecasting model.

Handles the full ML lifecycle:
  1. Download historical data from Yahoo Finance
  2. Train a Prophet model on adjusted closing prices
  3. Serialize the trained model to disk
  4. Generate forecasts for a specified horizon
"""

from __future__ import annotations

import datetime
import logging
from pathlib import Path

import joblib
import pandas as pd
import yfinance as yf
from prophet import Prophet

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve(strict=True).parent
TODAY = datetime.date.today()
TRAIN_START = "2020-01-01"


def train(ticker: str = "MSFT") -> None:
    """
    Train a Prophet model on historical stock data and save to disk.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol (e.g., MSFT, AAPL, GOOG).
    """
    logger.info("Downloading %s data from %s to %s", ticker, TRAIN_START, TODAY)
    data = yf.download(ticker, TRAIN_START, TODAY.strftime("%Y-%m-%d"))

    df = data.reset_index()[["Date", "Adj Close"]].rename(
        columns={"Date": "ds", "Adj Close": "y"}
    )

    model = Prophet()
    model.fit(df)

    model_path = BASE_DIR / f"{ticker}.joblib"
    joblib.dump(model, model_path)
    logger.info("Model saved to %s", model_path)


def predict(ticker: str = "MSFT", days: int = 7) -> list[dict] | bool:
    """
    Load a trained model and forecast future stock prices.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol matching a previously trained model.
    days : int
        Number of days to forecast into the future.

    Returns
    -------
    list[dict] or False
        Forecast records, or False if no trained model exists.
    """
    model_path = BASE_DIR / f"{ticker}.joblib"
    if not model_path.exists():
        logger.warning("No model found at %s", model_path)
        return False

    model = joblib.load(model_path)

    future_date = TODAY + datetime.timedelta(days=days)
    dates = pd.date_range(start=TRAIN_START, end=future_date.strftime("%Y-%m-%d"))
    df = pd.DataFrame({"ds": dates})

    forecast = model.predict(df)
    return forecast.tail(days).to_dict("records")


def convert(prediction_list: list[dict]) -> dict[str, float]:
    """
    Convert Prophet forecast records to a simple date → trend mapping.

    Parameters
    ----------
    prediction_list : list[dict]
        Raw Prophet forecast output.

    Returns
    -------
    dict[str, float]
        Mapping of date strings to predicted trend values.
    """
    return {
        record["ds"].strftime("%m/%d/%Y"): round(record["trend"], 2)
        for record in prediction_list
    }


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Train and predict stock prices")
    parser.add_argument("--ticker", type=str, default="MSFT", help="Stock ticker symbol")
    parser.add_argument("--days", type=int, default=7, help="Days to forecast")
    args = parser.parse_args()

    train(args.ticker)
    results = predict(ticker=args.ticker, days=args.days)
    if results:
        print(convert(results))
