import streamlit as st
import requests
import json

# Get the current price of Bitcoin
def get_bitcoin_price():
  response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot")
  data = json.loads(response.content)
  return data["amount"]

# Create a real-time graph of the Bitcoin price
def create_graph():
  st.line_chart(get_bitcoin_price(), xaxis_label="Time", yaxis_label="Price (USD)")

# Display the price of Bitcoin in number of bitcoin
def display_price_in_bitcoin():
  price = get_bitcoin_price()
  st.write("The price of Bitcoin is currently $" + str(price))
  st.write("This is equivalent to " + str(price / 1) + " bitcoin.")

# Main function
def main():
  create_graph()
  display_price_in_bitcoin()

if __name__ == "__main__":
  main()
