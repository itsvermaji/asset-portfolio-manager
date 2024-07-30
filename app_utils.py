import yfinance as yf
from models import *


def write_to_portfolio_sheet(sheet, holdings, skip_cols):
    sheet.update('A{}:E{}'.format(skip_cols + 1, len(holdings) + skip_cols), [[*holding] for holding in holdings])


# print(asyncio.run(get_ticker_price("ADANIPORTS.NS", "mf")))

def is_transaction_applicable(period, transaction):
    if (period == transaction.date):
        return False
    return False


def update_portfolio(ticker_details_map, holdings_map, financial_data, date, balance, invested_money, transactions):
    # do the update
    # print("transactions")
    # for txn in transactions:
    #     print(txn)

    if transactions:
        for txn in transactions:
            if txn.txn_type.lower() == "equity_bal_deposit":
                balance += txn.price
                invested_money += txn.price
                continue

            elif txn.txn_type.lower() == "equity_ref_bank":
                balance -= txn.price
                invested_money -= txn.price
                continue


            ticker = txn.ticker
            company_name = ticker_details_map.get(ticker).company_name
            holding = holdings_map.get(ticker)  # holding tells company has been traded in the past


            if txn.txn_type.lower() == "buy":
                if holding is None:
                    # holding hasn't been traded so far by us
                    holdings_map[ticker] = Holdings(company_name, ticker, txn.qty, txn.price)
                else:
                    # holding exists
                    qty = holding.qty
                    avg_price = holding.avg_price
                    holding.avg_price = (qty * avg_price + txn.qty * txn.price) / (qty + txn.qty)
                    holding.qty += txn.qty

                balance -= txn.qty * txn.price

            elif txn.txn_type.lower() == "sell":
                if holding is None:
                    raise Exception(
                        "The buy order for {0} is not found, Please check!".format(company_name))
                elif holding.qty < txn.qty:
                    raise Exception(
                        "The sell order quantity for {0} exceeds the stocks quantity in your portfolio, Please check!".format(company_name))
                else:
                    holding.qty -= txn.qty
                    holding.past_gains += (txn.price - holding.avg_price) * txn.qty  # gains will be recorded as past gains
                    balance += txn.qty * txn.price

    # updating portfolio with current share price
    [set_price(financial_data, date, holding) for holding in holdings_map.values() if holding.qty > 0]


def set_price(data, date, holding):
    # print("price_data", holding, date, holding.ticker, data.get(holding.ticker))

    # if date is not available
    last_available_date = date
    while (not data[holding.ticker].get(last_available_date.strftime("%Y-%m-%d"))):
        last_available_date -= datetime.timedelta(days=1)

    holding.curr_price = data[holding.ticker][last_available_date.strftime("%Y-%m-%d")]
    holding.curr_gains = holding.qty * (holding.curr_price - holding.avg_price)


def is_market_closed(financial_data, date):
    # all the tickers data is not available on that date
    # then markets are closed
    date = date.strftime('%Y-%m-%d')

    count = 0
    for comp in financial_data.values():
        if not comp.get(date):
            count += 1

    return True if count == len(financial_data.keys()) else False

def get_tickers_in_range(txn_list, start_date, end_date, holdings={}):
    # will return all the transacted tickers from start_date till end_date (end_date not including)
    tickers = set()
    for txn in txn_list:
        if txn.txn_type.lower() == 'equity_ref_bank' or txn.txn_type.lower() == 'equity_bal_deposit':
            continue
        if start_date <= txn.date < end_date:
            tickers.add(txn.ticker)

    if len(holdings.keys()) != 0:
        for holding in holdings.values():
            tickers.add(holding.ticker)

    return tickers

def get_metrics_from_portfolio(all_ticker_details, holdings):
    metrics = {}
    for ticker in holdings.keys():
        ticker_details = all_ticker_details.get(ticker)
        holding = holdings[ticker]

        # investment type metric
        metric_name = ticker_details.investmentType
        metric = metrics.get(metric_name)
        if not metric:
            # create that metric
            metrics[metric_name] = Metric(metric_name)
            metric = metrics[metric_name]

        # now add rest of the information
        metric.curr_gains += holding.curr_gains
        metric.past_gains += holding.past_gains
        metric.total_gains = metric.curr_gains + metric.past_gains
        metric.curr_amt += holding.curr_price + holding.past_gains
        metric.invested_amt = metric.curr_amt - metric.total_gains
        metric.gains_percent = (metric.curr_amt - metric.invested_amt)/metric.invested_amt

        # sector type metric
    return metrics


# def is_equity(inp):
#     if inp.lower() is 'equity':
#         return True
#     return False
#
# def is_mf(inp):
#     if inp.lower() == 'mf' or inp.lower() == 'mutualfund' or inp.lower() == 'mutual fund' or inp.lower() == 'mutual_fund' or inp.lower() == 'm f':
#         return True
#     return False