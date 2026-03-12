# Stock Price Predictor

Time series stock price forecasting API powered by Facebook Prophet, served via FastAPI with Docker support.

## How It Works

[Prophet](https://facebook.github.io/prophet/) models time series as an additive combination of components:

```
y(t) = trend(t) + seasonality(t) + holidays(t) + error(t)
```

The pipeline:

```
Yahoo Finance ──▶ Prophet Training ──▶ Model Serialization ──▶ FastAPI Serving
(historical data)   (fit trend +         (joblib)              (REST predictions)
                     seasonality)
```

1. **Data Ingestion** — Downloads historical adjusted closing prices from Yahoo Finance via `yfinance`
2. **Model Training** — Fits a Prophet model capturing trend and seasonal patterns
3. **Serialization** — Saves the trained model using `joblib` for fast loading
4. **Serving** — FastAPI endpoint loads the model and generates forecasts on demand

## API Reference

### `POST /predict`

**Request:**
```json
{
  "ticker": "AAPL",
  "days": 7
}
```

**Response:**
```json
{
  "ticker": "AAPL",
  "days": 7,
  "forecast": {
    "03/06/2024": 171.42,
    "03/07/2024": 171.58,
    "03/08/2024": 171.73,
    "03/09/2024": 171.89,
    "03/10/2024": 172.05,
    "03/11/2024": 172.20,
    "03/12/2024": 172.36
  }
}
```

## Sample Predictions

The `plots/` directory contains forecast visualizations for AAPL, MSFT, and GOOG showing predicted trends with component decomposition.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Forecasting | Facebook Prophet |
| Data Source | Yahoo Finance (yfinance) |
| API Framework | FastAPI + Uvicorn |
| Serialization | joblib |
| Containerization | Docker |

## Quick Start

### Docker

```bash
docker build -t stock-predictor .
docker run -p 8000:8000 stock-predictor
```

### Local

```bash
pip install -r requirements.txt

# Train a model
python src/model.py --ticker AAPL --days 30

# Start the API server
cd src && uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Interactive docs: `http://localhost:8000/docs`

## Project Structure

```
stock-predictor/
├── src/
│   ├── main.py         # FastAPI application
│   ├── model.py        # Prophet training and prediction logic
│   └── schemas.py      # Pydantic request/response models
├── plots/              # Sample forecast visualizations
│   ├── AAPL_plot.png
│   ├── MSFT_plot.png
│   └── GOOG_plot.png
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

## Prophet vs. ARIMA vs. LSTM

| Feature | Prophet | ARIMA | LSTM |
|---------|---------|-------|------|
| **Approach** | Additive regression with Fourier seasonality | Statistical autoregressive model | Neural network with memory cells |
| **Strengths** | Handles missing data, holidays, changepoints automatically | Well-understood theory, works well on stationary data | Can learn complex nonlinear patterns |
| **Weaknesses** | Less control over model internals | Requires stationarity, manual parameter tuning | Needs large datasets, prone to overfitting |
| **Best For** | Business forecasting with strong seasonality | Short-term forecasting of stationary series | Large-scale sequential pattern learning |

Prophet was chosen for this project because stock price data exhibits strong weekly and yearly seasonality, and Prophet handles this natively without manual seasonal decomposition.

## License

MIT
