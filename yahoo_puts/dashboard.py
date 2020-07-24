import streamlit as st
import yfinance as yf


@st.cache
def get_ticker(ticker: str, call_put: str, time: str):
    chain = ticker.option_chain(time)
    return chain.calls if call_put == 'calls' else chain.puts


stocks = ['TSLA', 'JWN', 'AAPL']
table_type = ['calls', 'puts']

st.write('Hello World')

ticker = st.sidebar.selectbox(
    'Pick a ticker',
    stocks
)

call_put = st.sidebar.selectbox(
    'Choose a type',
    table_type
)

cur_ticker = yf.Ticker(ticker)
options_dates = cur_ticker.options

date = st.sidebar.selectbox(
    'Choose a date',
    options_dates
)

st.dataframe(get_ticker(cur_ticker, call_put, date))
