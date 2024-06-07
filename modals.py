class TransactionDetails:
    def __init__(self, company_name, qty, txn_type, price, date):
        self.company_name = company_name
        self.qty = float(qty)
        self.txn_type = txn_type
        self.price = float(price)
        self.date = date

    def __str__(self):
        return '[company: {0}, quantity: {1}, txnType: {2}, price: {3}, date: {4}]'.format(self.company_name, self.qty, self.txn_type, self.price, self.date)

class TickerDetails:
    def __init__(self, company_name, ticker, investmentType, sector, mktCap, source):
        self.company_name = company_name
        self.ticker = ticker
        self.investmentType = investmentType
        self.sector = sector
        self.mktCap = mktCap
        self.source = source
    
    def __str__(self):
        return '[company: {0}, ticker: {1}, investmentType: {2}, sector: {3}, mktCap: {4}, source: {5}]'.format(self.company_name, self.ticker, self.investmentType, self.sector, self.mktCap, self.source)

class Holdings:
    def __init__(self, company_name, qty, avgPrice, currPrice, gains):
        self.company_name = company_name
        self.qty = float(qty)
        self.avgPrice = float(avgPrice)
        self.currPrice = float(currPrice)
        self.gains = gains
    
    def __str__(self):
        return '[company: {0}, quantity: {1}, avg price: {2}, current price: {3}, gains: {4}]'.format(self.company_name, self.qty, self.avgPrice, self.currPrice, self.gains)

class Metric:
    def __init__(self, name, initial_amt, total_amt, total_gains):
        self.name = name
        self.initial_amt = initial_amt
        self.total_amt = total_amt
        self.total_gains = total_gains
