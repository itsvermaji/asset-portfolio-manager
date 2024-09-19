import json

import gspread
import asyncio
from influxdb_client.client.write_api import SYNCHRONOUS

from collections import OrderedDict, defaultdict
from variables import *
from financial_data import *
from app_utils import *
from models import *
from app_configs import *

gc = gspread.service_account(filename='./investment_sheet_credentials.json')
sheet = gc.open_by_key('1ULwxbzQW8jzLWlinOTyHCjAglObrSw1YUiszk18ots0')

# getting sheets
transactions_sheet = sheet.worksheet("Transactions")
portfolio_sheet = sheet.worksheet("Portfolio")
ticker_details_sheet = sheet.worksheet("Ticker Details")
daily_returns_sheet = sheet.worksheet('Daily Returns 2')

# reading ticker details
ticker_details_list = ticker_details_sheet.get_all_values()
all_ticker_details = [TickerDetails(*x) for x in ticker_details_list[1:]]
ticker_details_map = {}
for t_detail in all_ticker_details:
    ticker_details_map[t_detail.ticker] = t_detail

# [print(x) for x in all_ticker_details]

# reading transaction sheet
raw_transactions = transactions_sheet.get_all_values()
transactions_list = [TransactionDetails(*x) for x in raw_transactions[1:]]
transactions_list.reverse()
# [print(x) for x in transactions]

# get date wise mapping
period_txns_mapping = defaultdict(list)

for transaction in transactions_list:
    period = transaction.date
    period_txns_mapping[period].append(transaction)


def fun(x):
    [print(y, end=", ") for y in x]
    print()


# [fun(x) for x in period_txns_mapping.values()]

# getting current holdings
# loop over everydate.
holdings_map = {}
balance = 0
invested_money = 0


async def update_portfolio_till_today():
    # ticker_details_map, holdings_map, transactions = [], update_tickers_price = True
    metrics = reset_metrics(ticker_details_map)
    start_date = updatedOn + datetime.timedelta(days=1)
    end_date = datetime.date(2024, 8, 31)
    # metrics = {
    #     'equity': Metric("equity"),
    #     'mf': Metric("mf")
    # }

    # range will be from [start_date, end_date), excluding end_date
    tickers_list = get_tickers_in_range(transactions_list, start_date, end_date, holdings_map)
    # map<string, map<date, integer>> Map of companies value being date vs price map.
    financial_data = get_price_history(tickers_list, start_date, end_date)
    # # saving data
    json_data = json.dumps(financial_data, indent=4)
    f = open('financial_data.json', 'a')
    f.write(json_data)
    f.close()


    # getting data from file
    # f = open('financial_data.json')
    # financial_data = json.load(f)


    # financial_data = {}
    await asyncio.sleep(1)
    # print("financial_data", financial_data)

    metrics_to_write = []
    while start_date <= end_date:
        # skip saturdays and sundays
        # if is_market_closed(financial_data, start_date):
        #     start_date += datetime.timedelta(days=1)
        #     continue

        # optimize the financial_data structure
        txns = [] if not period_txns_mapping.get(start_date) else period_txns_mapping[start_date]
        update_portfolio(txns, start_date, ticker_details_map, holdings_map, financial_data, metrics)

        # printing the portfolio
        # print("portfolio on date", date, "balance", balance)
        # for holding in holdings_map.values():
        #     print(holding, end=" ")
        # print()

        # collecting metrics
        app_metrics = get_metrics_from_portfolio(ticker_details_map, holdings_map)
        metrics_list = [start_date.isoformat(), *get_metrics_as_list(app_metrics)]
        metrics_to_write.append(metrics_list)

        # print(metrics)
        # equity = metrics['equity']

        # [print(ticker) for ticker in get_current_portfolio(holdings_map)]
        print(start_date.isoformat())

        print_current_portfolio(holdings_map)

        # print(f'Date: {start_date}, total val: {equity.total_val}, standing val: {equity.standing_val}, invested_amt: {equity.invested_amt}, '
        #       f'total_gains: {equity.total_gains}, balance: {equity.balance}')
        # print(end="\n\n")

        start_date += datetime.timedelta(days=1)

    # write current portfolio
    curr_holdings = [holding for holding in holdings_map.values() if holding.qty > 0]
    write_to_portfolio_sheet(portfolio_sheet, curr_holdings, ticker_details_map, 1)

    # write past portfolio
    past_holdings = [holding for holding in holdings_map.values() if holding.qty <= 0]
    skip_cols = len(curr_holdings) + 5
    write_to_portfolio_sheet(portfolio_sheet, past_holdings, ticker_details_map, skip_cols)

    # writing to daily returns sheet
    write_to_daily_returns_sheet(daily_returns_sheet, metrics_to_write)


asyncio.run(update_portfolio_till_today())
# update_portfolio_till_today()
