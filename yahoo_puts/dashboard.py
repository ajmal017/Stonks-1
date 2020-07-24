from PIL import Image
import streamlit as st
import yfinance as yf


@st.cache
def get_ticker(ticker: str, call_put: str, time: str):
    chain = ticker.option_chain(time)
    return chain.calls if call_put == 'calls' else chain.puts


table_type = ['calls', 'puts']

stonks = Image.open('media/stonks.jpg')
st.write('Welcome to Stonks')
st.image(stonks)


ticker: str = st.sidebar.text_input('Type a ticker symbol', 'TSLA')

ticker.upper()

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
