from PIL import Image
import pandas as pd
import streamlit as st
import yfinance as yf
import base64
from dataclasses import dataclass
from enum import Enum
from math import ceil


class TradeType(Enum):
    call = 0
    put = 1


class BuySell(Enum):
    buy = 0
    sell = 1


@dataclass
class Trade:
    trade_type: TradeType
    buy_sell: BuySell
    num_contracts: int
    strike_price: int
    premium: float


def format_type(v: str):
    new = v.lower()
    if new == 'call':
        return TradeType.call
    if new == 'put':
        return TradeType.put
    if new == 'buy':
        return BuySell.buy
    if new == 'sell':
        return BuySell.sell


@st.cache
def get_ticker(ticker: str, call_put: TradeType, time: str) -> pd.DataFrame:
    chain = ticker.option_chain(time)
    if call_put == TradeType.call:
        return chain.calls
    if call_put == TradeType.put:
        return chain.puts


@st.cache
def get_table_download_link(df, call_put: TradeType):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}">Download {"calls" if call_put == TradeType.call else "puts"} csv file</a>'


stonks = Image.open('media/stonks.jpg')
st.write('Welcome to Stonks')
st.image(stonks)


# define sidebar controls
ticker: str = st.sidebar.text_input('Type a ticker symbol', 'TSLA')
ticker.upper()

# call_put = st.sidebar.selectbox(
#     'Choose a type',
#     table_type
# )

cur_ticker = yf.Ticker(ticker)
options_dates = cur_ticker.options
date = st.sidebar.selectbox(
    'Choose a date',
    options_dates
)

num_trades = st.sidebar.number_input('Number of Trades', 1, None)


# get stock data
call_frame: pd.DataFrame = get_ticker(cur_ticker, TradeType.call, date)
put_frame: pd.DataFrame = get_ticker(cur_ticker, TradeType.put, date)


# write dataframe and downloader
st.markdown('# Calls')
st.dataframe(call_frame)
st.markdown('# Puts')
st.dataframe(put_frame)
st.markdown(get_table_download_link(call_frame, TradeType.call), unsafe_allow_html=True)
st.markdown(get_table_download_link(put_frame, TradeType.put), unsafe_allow_html=True)


trades = []
for i in range(num_trades):
    st.markdown('---')
    st.markdown(f'# Trade {i + 1}')
    buy_sell: str = format_type(st.selectbox(
        'Buy or sell',
        ('Buy', 'Sell'),
        key=f'{i}buy_sell'
    ))
    # acc.append({'buy_sell': buy_sell})

    num_contracts = st.number_input('Input Number of Contracts', 1, None, 1, key=f'{i}contracts')

    call_put: TradeType = format_type(st.selectbox(
        'Call or Put',
        ('Call', 'Put'),
        key=f'{i}call_put'
    ))
    # acc[i - 1]['num_contracts'] = num_contracts

    this_trade = call_frame if call_put == TradeType.call else put_frame
    series = this_trade['strike']
    strike = st.number_input(
        'Input Strike Price',
        int(min(series)),
        int(max(series)),
        key=f'{i}strike'
    )
    # acc[i - 1]['strike'] = strike
    try:
        # tmp = acc[i - 1]['buy_sell']
        bid_ask = "ask" if buy_sell == BuySell.buy else "bid"
        premium = this_trade.loc[this_trade['strike'] == strike, bid_ask].values[0]
        st.write(f'You {"pay" if buy_sell == BuySell.buy else "receive"} {premium * num_contracts}')

        # cache data to list of trades
        trades.append(Trade(call_put, buy_sell, num_contracts, strike, premium))
    except IndexError:
        st.write('Strike price not found in table')


st.markdown('---')
st.markdown('# Pricing Outcome')
# buy = premium = ask
# sell = premium = bid

# get ascending list of all strike prices
@st.cache
def get_strike_prices_range(call: int, put: int):
    overall = max(call, put)
    return range(0, ceil(overall * 1.5), 100)


def calcuate_value(this_price: int, trade: Trade, call: pd.DataFrame, put: pd.DataFrame):
    if trade.trade_type == TradeType.call:
        if trade.buy_sell == BuySell.buy:
            return -1 * trade.premium if this_price <= trade.strike_price else (this_price - trade.strike_price) - trade.premium

        if trade.buy_sell == BuySell.sell:
            return trade.premium if this_price <= trade.strike_price else trade.premium - (this_price - trade.strike_price)

    if trade.trade_type == TradeType.put:
        if trade.buy_sell == BuySell.buy:
            return -1 * trade.premium if this_price >= trade.strike_price else (trade.strike_price - this_price) - trade.premium

        if trade.buy_sell == BuySell.sell:
            return trade.premium if this_price >= trade.strike_price else trade.premium - (trade.strike_price - this_price)


strike_price_range = get_strike_prices_range(call_frame['strike'].max(), put_frame['strike'].max())


chart_data = pd.DataFrame(
    [{f"Trade {i + 1}": calcuate_value(x, y, call_frame, put_frame) for i, y in enumerate(trades)} for x in strike_price_range],
    index=strike_price_range
)
st.line_chart(chart_data)

