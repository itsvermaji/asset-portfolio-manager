import yfinance as yf
import asyncio

async def get_ticker_price(ticker, type):
    info = yf.Ticker(ticker).info
    # print(info)
    return float(info['currentPrice']) if type.lower() == "equity" else float(info['previousClose'])

def write_to_portfolio_sheet(sheet, holdings, skip_cols):
    sheet.update('A{}:E{}'.format(skip_cols+1, len(holdings) + skip_cols), [[*holding] for holding in holdings])

# print(asyncio.run(get_ticker_price("ADANIPORTS.NS", "mf")))
