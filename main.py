import gspread
from modals import *
from utils import *
import asyncio
from collections import OrderedDict

gc = gspread.service_account(filename='./investment_sheet_credentials.json')
sheet = gc.open_by_key('1ULwxbzQW8jzLWlinOTyHCjAglObrSw1YUiszk18ots0')

# getting sheets
transactions_sheet = sheet.worksheet("Transactions")
portfolio_sheet = sheet.worksheet("Current Holdings")
ticker_details_sheet = sheet.worksheet("Ticker Details")

# reading ticker details
ticker_details_list = ticker_details_sheet.get_all_values()
all_ticker_details = [TickerDetails(*x) for x in ticker_details_list[1:]]
ticker_details_map = {}
for ticker in all_ticker_details:
    ticker_details_map[ticker.company_name] = ticker

# [print(x) for x in all_ticker_details]

# reading transaction sheet
transactions_list = transactions_sheet.get_all_values()
transactions = [TransactionDetails(*x) for x in transactions_list[1:]]
transactions.reverse()
# [print(x) for x in transactions]

holdings_map = OrderedDict()

for txn in transactions:
    comp = txn.company_name
    if holdings_map.get(comp):
        prev_holding = holdings_map[comp]
        if txn.txn_type.lower() == "buy":
            new_price = (prev_holding.avgPrice * prev_holding.qty + txn.price * txn.qty)/(prev_holding.qty + txn.qty)
            prev_holding.qty = prev_holding.qty + txn.qty
            prev_holding.avgPrice = new_price
            prev_holding.gains -= txn.qty * txn.price
        else: 
            prev_holding.gains = prev_holding.gains + txn.qty * txn.price
            prev_holding.qty = prev_holding.qty - txn.qty
    else:
        (ticker, type) = [ticker_details_map.get(comp).ticker, ticker_details_map.get(comp).investmentType]
        currPrice = asyncio.run(get_ticker_price(ticker, type))
        new_qty = txn.qty if txn.txn_type.lower() == "buy" else -1 * txn.qty
        new_gains = txn.price * txn.qty * (-1 if txn.txn_type.lower() == "buy" else 1)
        holdings_map[comp] = Holdings(txn.company_name, new_qty, txn.price, currPrice, new_gains)

    # print(holdings_map[comp])

# holdings_map = sorted(holdings_map.items(), key=lambda kv: kv[1])
holdings_map = dict([[key, holdings_map[key]] for key in sorted(holdings_map.keys())])
# [print(val) for key, val in holdings_map.items()]

# adjusting current gains
for holding in holdings_map.values():
    holding.gains += holding.qty * holding.currPrice

# Writing to Holdings Sheet
skip_cols = 1
current_holdings = [[holding.company_name, holding.qty, holding.avgPrice, holding.currPrice, holding.gains] for holding in holdings_map.values() if holding.qty > 0]
past_holdings = [[holding.company_name, holding.qty, holding.avgPrice, holding.currPrice, holding.gains] for holding in holdings_map.values() if holding.qty <= 0]
write_to_portfolio_sheet(portfolio_sheet, current_holdings, skip_cols)
write_to_portfolio_sheet(portfolio_sheet, past_holdings, skip_cols + 2 + len(current_holdings))


# # sector wise gains
# metric_tracker = {}
# for company_details in ticker_details_map.values():
#     if(company_details.sector):
#         metric_tracker[company_details.sector] = Metric(company_details.sector, 0, 0, 0)

# # investment type wise gains
# investment_type_gains = {}
# for company_details in ticker_details_map.values():
#     if(company_details.investmentType):
#         metric_tracker[company_details.investmentType] = Metric(company_details.investmentType, 0, 0, 0)


# # reading from backup
# backup_data = {}
# for data in open('backup.csv', 'r').readlines():
#     [metric_name, initial_amt, total_amt, total_gains] = print(data.split(','))
#     metric_name = metric_name.strip()
#     initial_amt = int(initial_amt.strip())
#     total_amt = int(total_amt.strip())
#     total_gains = int(total_gains.strip())
#     backup_data[metric_name] = Metric(metric_name, initial_amt, total_amt, total_gains)

# # print(text)



