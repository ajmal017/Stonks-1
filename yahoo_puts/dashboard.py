from PIL import Image
import streamlit as st
import yfinance as yf
import base64


@st.cache
def get_ticker(ticker: str, call_put: str, time: str):
    chain = ticker.option_chain(time)
    return chain.calls if call_put == 'calls' else chain.puts


@st.cache
def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'


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

cur_frame = get_ticker(cur_ticker, call_put, date)

st.dataframe(cur_frame)

buy_sell: str = st.selectbox(
    'Buy or sell',
    ('Buy', 'Sell')
)

num_contracts = st.number_input('Input Number of Contracts', 1, None, 1)

price = st.number_input(
    'Input Strike Price',
    int(min(cur_frame['strike'])),
    int(max(cur_frame['strike']))
)
new_df = cur_frame.loc[cur_frame['strike'] == price]
try:
    price = new_df["ask" if buy_sell == "Buy" else "bid"].tolist()[0]
    st.write(f'You {"pay" if buy_sell == "Buy" else "receive"} {price * num_contracts}')
except IndexError:
    st.write('Strike price not found in table')

st.markdown(get_table_download_link(cur_frame), unsafe_allow_html=True)



