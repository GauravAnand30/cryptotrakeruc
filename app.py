import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import plotly.express as px
from streamlit_lottie import st_lottie
import requests

# Function to load Lottie animations from a URL
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load a Lottie animation
lottie_crypto = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_rggj5r1z.json")

# Define crypto mappings
crypto_mapping = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Ripple": "XRP-USD",
    "Litecoin": "LTC-USD",
    "Cardano": "ADA-USD"
}

st.markdown("""
    <style>
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }

    .main-title {
        color: #FF4500;
        animation: fadeIn 2s ease-in-out;
    }

    .sidebar .sidebar-content {
        animation: fadeIn 2s ease-in-out;
        background-color: #f4f4f4;
    }

    .sidebar .sidebar-content h2 {
        font-size: 20px;
        color: #FF4500;
        margin-bottom: 20px;
    }

    .sidebar .sidebar-content div {
        font-size: 18px;
        color: #333;
        margin-bottom: 10px;
    }

    .sidebar .sidebar-content div label {
        color: #333;
        font-weight: bold;
    }

    .sidebar .sidebar-content div .stDateInput,
    .sidebar .sidebar-content div .stSelectbox {
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 5px;
    }

    .stButton>button {
        background-color: #FF4500;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #e63e00;
    }

    .stPlotlyChart {
        animation: fadeIn 2s ease-in-out;
    }

    footer {visibility: hidden;}
    .stApp {bottom: 80px;}
    footer:after {
        content:'Crypto Tracker App by Your Name'; 
        visibility: visible;
        display: block;
        position: relative;
        color: tomato;
        padding: 5px;
        top: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📈 Crypto Tracker</h1>", unsafe_allow_html=True)
st.markdown("<h2>Track your favorite cryptocurrency with ease and visualize its historical data.</h2>", unsafe_allow_html=True)

st.sidebar.header("Configuration")
crypto_option = st.sidebar.selectbox(
    "Which Crypto do you want to visualize?", ("Bitcoin", "Ethereum", "Ripple", "Litecoin", "Cardano")
)

start_date = st.sidebar.date_input("Start Date", date.today() - relativedelta(months=1))
end_date = st.sidebar.date_input("End Date", date.today())

data_interval = st.sidebar.selectbox(
    "Data Interval",
    (
        "1m",
        "2m",
        "5m",
        "15m",
        "30m",
        "60m",
        "90m",
        "1h",
        "1d",
        "5d",
        "1wk",
        "1mo",
        "3mo",
    ),
)

symbol_crypto = crypto_mapping[crypto_option]
data_crypto = yf.Ticker(symbol_crypto)

value_selector = st.sidebar.selectbox(
    "Value Selector", ("Open", "High", "Low", "Close", "Volume")
)

if st.sidebar.button("Generate"):
    crypto_hist = data_crypto.history(
        start=start_date, end=end_date, interval=data_interval
    )
    
    # Generate the plot for selected crypto
    fig = px.line(
        crypto_hist,
        x=crypto_hist.index,
        y=value_selector,
        labels={"x": "Date", value_selector: f"{crypto_option} {value_selector}"},
        title=f"{crypto_option} {value_selector} from {start_date} to {end_date}",
    )
    fig.update_layout(xaxis_title="Date", yaxis_title=f"{crypto_option} {value_selector}")

    # Display the plot with animation if available
    if lottie_crypto:
        st_lottie(lottie_crypto, height=200, key="crypto")
    st.plotly_chart(fig)

    # Display details below the graph
    st.markdown(f"### {crypto_option} {value_selector} Data")
    st.write(f"**Start Date:** {start_date}")
    st.write(f"**End Date:** {end_date}")
    st.write(f"**Data Interval:** {data_interval}")
    st.write(f"**Number of Data Points:** {len(crypto_hist)}")

    st.dataframe(crypto_hist[[value_selector]])

    # Generate additional plot for Bitcoin market value changes
    if crypto_option != "Bitcoin":
        bitcoin_hist = yf.Ticker("BTC-USD").history(start=start_date, end=end_date, interval=data_interval)
        fig_bitcoin = px.line(
            bitcoin_hist,
            x=bitcoin_hist.index,
            y="Close",
            labels={"x": "Date", "Close": "Bitcoin Close Value"},
            title=f"Bitcoin Close Value from {start_date} to {end_date}",
        )
        fig_bitcoin.update_layout(xaxis_title="Date", yaxis_title="Bitcoin Close Value")
        st.plotly_chart(fig_bitcoin)

        st.markdown(f"### Bitcoin Close Value Data")
        st.write(f"**Start Date:** {start_date}")
        st.write(f"**End Date:** {end_date}")
        st.write(f"**Data Interval:** {data_interval}")
        st.write(f"**Number of Data Points:** {len(bitcoin_hist)}")

        st.dataframe(bitcoin_hist[["Close"]])
