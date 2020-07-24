import yfinance as yf
from pandas import ExcelWriter


stocks = ['TSLA', 'JWN', 'AAPL']
output_frames = {}
for stock in stocks:
    cur = yf.Ticker(stock)

    options_dates = cur.options

    index_list = [1, 4, 7]

    for i in index_list:
        opt_chain = cur.option_chain(options_dates[i])
        output_frames[f"{stock}_{options_dates[i]}_puts"] = opt_chain.puts
        output_frames[f"{stock}_{options_dates[i]}_calls"] = opt_chain.calls


with ExcelWriter('alvin.xlsx') as writer:
    for name, df in output_frames.items():
        print(df)
        df.to_excel(writer, name)
