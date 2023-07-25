import time
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import requests
import json
from prophet import Prophet
from plotly import graph_objs as go

# Set up the Streamlit layout
st.title('Real-time Bitcoin Price')
price_text = st.empty()
prediction_text = st.empty()
graph_placeholder = st.empty()

# Function to get current bitcoin price


def get_bitcoin_price():
    response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot")
    data = json.loads(response.text)
    return round(float(data["data"]["amount"]), 2)

# Function to get historical bitcoin price


def get_historical_bitcoin_price():
    # Get data from the last 15 minutes
    url = "https://min-api.cryptocompare.com/data/v2/histominute?fsym=BTC&tsym=USD&limit=1"
    response = requests.get(url)
    data = response.json()['Data']['Data']

    # Create a DataFrame
    price_data = pd.DataFrame(data)
    price_data['time'] = pd.to_datetime(price_data['time'], unit='s')


    price_data = price_data.rename(columns={'time': 'time', 'close': 'price'})

    return price_data[['time', 'price']]


# Fetch historical data for the last 15 minutes
price_data = get_historical_bitcoin_price()

# Create a plotly figure with an initial trace
fig = go.Figure(data=[go.Scatter(x=price_data['time'],
                y=price_data['price'], mode='lines', name='Actual')])

# Initialize Prophet model
m = Prophet()

# Variables to control the prediction timing
start_time = time.time()
prediction_interval = 5  # predict every 60 seconds

# Update the Bitcoin price every second and make predictions every minute
while True:
    # Get the current price
    price = get_bitcoin_price()

    # Update the price text
    price_text.text(f'Current Bitcoin price: ${price}')

    # Append the current price and time to the DataFrame
    price_data = pd.concat([price_data, pd.DataFrame(
        {'time': [datetime.now()], 'price': [price]})], ignore_index=True)

    # Remove data older than 60 minutes
    price_data = price_data[price_data['time'] >
                            (datetime.now() - timedelta(minutes=60))]

    # Check if it's time to make a prediction
    if time.time() - start_time > prediction_interval:
        # Reset the timer
        start_time = time.time()

        # Fit the Prophet model
        m = Prophet()
        m.fit(price_data.rename(columns={'time': 'ds', 'price': 'y'}))

        # Make a future dataframe for 15 seconds
        future = m.make_future_dataframe(periods=1, freq='10S')

        # Make predictions
        forecast = m.predict(future)

        # Keep only the prediction for the next minute
        prediction = forecast.loc[forecast['ds'] ==
                                  forecast['ds'].max(), ['ds', 'yhat']]

        # Update the prediction text
        prediction_text.text(
            f'Predicted Bitcoin price for the next minute: ${round(prediction["yhat"].values[0], 2)}')

        # Add the predictions to the plot
        if len(fig.data) > 1:
            fig.data[1].x = list(fig.data[1].x) + \
                prediction['ds'].dt.to_pydatetime().tolist()
            fig.data[1].y = list(fig.data[1].y) + prediction['yhat'].tolist()
        else:
            fig.add_trace(go.Scatter(
                x=prediction['ds'], y=prediction['yhat'], mode='markers', name='Predicted', marker=dict(color='red')))

    # Update the data of the plotly figure's first trace (actual prices)
    fig.data[0].x = price_data['time']
    fig.data[0].y = price_data['price']

    # Display the plot in Streamlit
    graph_placeholder.plotly_chart(fig)

    # Wait for 1 second
    time.sleep(1)
