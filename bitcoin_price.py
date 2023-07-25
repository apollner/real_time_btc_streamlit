import time
import streamlit as st
import pandas as pd
import cryptocompare
from datetime import datetime
import plotly.graph_objects as go

# Create a dataframe to hold the Bitcoin price data
price_data = pd.DataFrame(columns=['time', 'price'])

# Create a plotly figure with an initial trace
fig = go.Figure(data=[go.Scatter(x=price_data['time'],
                y=price_data['price'], mode='lines')])

# Set up the Streamlit layout
st.title('Real-time Bitcoin Price')
price_text = st.empty()
graph_placeholder = st.empty()

# Update the Bitcoin price every second
while True:
    # Get the current price
    price = cryptocompare.get_price('BTC', currency='USD')['BTC']['USD']

    # Update the price text
    price_text.text(f'Current Bitcoin price: ${price}')

    # Append the current price and time to the dataframe
    price_data = price_data.append(
        {'time': datetime.now(), 'price': price}, ignore_index=True)

    # Update the data of the plotly figure's first trace
    fig.data[0].x = price_data['time']
    fig.data[0].y = price_data['price']

    # Display the plot in Streamlit
    graph_placeholder.plotly_chart(fig)

    # Wait for 1 second
    time.sleep(1)
