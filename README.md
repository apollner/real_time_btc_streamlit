
# Real-time Bitcoin Price Tracker and Predictor

This script creates a real-time Bitcoin price tracker and predictor. It fetches the current Bitcoin price in USD every few seconds and makes predictions for the future price. The script also maintains a rolling window of the last 60 minutes of data for prediction purposes.

This application uses:

- **Streamlit**: for creating and managing the web-based user interface.
- **Pandas**: for data manipulation and analysis.
- **Requests**: for making HTTP requests.
- **Prophet**: for making predictions based on the fetched data.
- **Plotly**: for creating interactive plots.

## Dependencies

To run this script, the following packages are required:

- streamlit
- pandas
- requests
- fbprophet
- plotly

You can install these packages using pip:

```
pip install streamlit pandas requests fbprophet plotly
```

## How it Works

The application uses two main functions:

- `get_bitcoin_price()`: This function makes a GET request to the Coinbase API to fetch the current Bitcoin price in USD.

- `get_historical_bitcoin_price()`: This function fetches historical Bitcoin price data from the CryptoCompare API. It returns a DataFrame containing the closing price for each minute of the last 15 minutes.

The script also includes a loop that runs indefinitely. This loop:

- Fetches the current Bitcoin price every second.
- Appends the current price and time to the DataFrame.
- Removes data older than 60 minutes from the DataFrame.
- Every minute, it fits a Prophet model to the data and makes a prediction for the price in the next minute.
- Updates the Plotly figure with the actual prices and the prediction.
- Waits for a second before repeating the process.

## Running the Script

You can run the script using the command:

```
streamlit run <filename.py>
```

Once the application is running, you can access it in your web browser. The application will display the current Bitcoin price, the predicted price for the next minute, and a plot of the historical and predicted prices.

Please note that the prediction functionality in this script is highly simplistic and should not be used for actual trading decisions. It is meant for educational and illustrative purposes only.

## Accessing the App

You can access the live app using the following link: [Real-time Bitcoin Price Tracker and Predictor](https://realtimebtcapp-5knbtx3e51y.streamlit.app/)
