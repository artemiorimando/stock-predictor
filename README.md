# stock-predictor

# Rubric Questions
## Algorithm Understanding
### How does the Prophet Algorithm differ from an LSTM?
The Prophet Algorithm differs from LSTM by the way the models are designed. LSTM is a neural network model and Prophet is a type of additive regression model that models using fourier transforms.
### Why does an LSTM have poor performance against ARIMA and Profit for Time Series?
LSTM has poor performance against ARIMA and Profit for Time Series because if the time series data cannot be completely modelled linearly and if the data is not completely stationary. Time series data that is super volatile or variable might be better learned by an LSTM model but would probably just be the cause of overfitting.

## Interview Readiness
### What is exponential smoothing and why is it used in Time Series Forecasting?
Exponential smoothing is a univariate time series technique that smooths out time series data using exponential window functions. It is used in Time Series forecasting because predictions are made using weights on past data where older data are weighted using an exponential decreasing weight.

## Interview Readiness
### What is stationarity? What is seasonality? Why Is Stationarity Important in Time Series Forecasting?
Stationarity is when time series data has a mean and variance that does not change over time. Seasonality is a characteristic of time series data where any predictable or reoccuring pattern in the data happens over time. Stationarity is important in Time Series Forecasting because many time series forecasting techniques depend on unchanging statistical properties of the data to be able to be modelled accordingly.

## Interview Readiness
How is seasonality different from cyclicality? Fill in the blanks:
___ is predictable, whereas ___ is not.

Seasonality is predictable, whereas cyclicality is not. Seasonality are observed patterns that happen over fixed times in a calendar year whereas cyclicality are observed patterns that happen over varyin (shorter or longer) time periods.
