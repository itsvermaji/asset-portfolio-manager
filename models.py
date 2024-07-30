import datetime


class TransactionDetails:
    def __init__(self, company_name, ticker, qty, txn_type, price, date):
        self.company_name = company_name
        self.ticker = ticker
        self.qty = float(qty)
        self.txn_type = txn_type
        self.price = float(price)

        # converting string date to date
        [dd, mm, yyyy] = [int(x) for x in date.split('/')]
        self.date = datetime.date(yyyy, mm, dd)

    def __str__(self):
        return '[company: {0}, ticker: {1}, quantity: {2}, txnType: {3}, price: {4}, date: {5}]'.format(
            self.company_name, self.ticker, self.qty, self.txn_type, self.price, self.date)


class TickerDetails:
    def __init__(self, company_name, ticker, investmentType, sector, mktCap, source):
        self.company_name = company_name
        self.ticker = ticker
        self.investmentType = investmentType
        self.sector = sector
        self.mktCap = mktCap
        self.source = source

    def __str__(self):
        return '[company: {0}, ticker: {1}, investmentType: {2}, sector: {3}, mktCap: {4}, source: {5}]'.format(
            self.company_name, self.ticker, self.investmentType, self.sector, self.mktCap, self.source)


class Holdings:
    curr_price = 0  # today's share price
    curr_gains = 0  # current gains in the current portfolio qty * (curr_price - avg_price)
    past_gains = 0  # gains calculated when the share is sold

    def __init__(self, company_name, ticker, qty, avg_price):
        self.company_name = company_name
        self.ticker = ticker
        self.qty = float(qty)
        self.avg_price = float(avg_price)

    def __str__(self):
        return '[company: {0}, quantity: {1}, avg price: {2}, current price: {3}, current_gains: {4}, past_gains: {5}]'.format(
            self.company_name, self.qty, self.avg_price, self.curr_price, self.curr_gains, self.past_gains)


class Metric:
    invested_amt = 0
    curr_amt = 0
    curr_gains = 0
    past_gains = 0
    total_gains = 0
    gains_percent = 0

    def __init__(self, name):
        self.name = name
