#import datetime functions
import datetime as dt
from datetime import date

class Investor:
    """Class to model an Investor account."""
    def __init__(self, investorID, acct_number, first_name, last_name, address, city, state, zip, phone):
        """Initialize investor attributes."""
        self.investorID = investorID
        self.acctNumber = acct_number
        self.firstName = first_name
        self.lastName = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zipCode = zip
        self.phoneNumber = phone
        self.stockPurchases = []
        self.bondPurchases = []

    def acctholder_info(self):
        """Create value for the investor name."""
        acctholder = f"{self.firstName.title()} {self.lastName.title()}"
        return acctholder

    def acctholder_addr(self):
        """Create value for the investor address."""
        acctAddress = f"{self.address.title()}, {self.city.title()}, {self.state.upper()} {self.zipCode}"
        return acctAddress

    def add_stockPurchase(self, stockPurchID):
        self.stockPurchases.append(stockPurchID)

    def add_bondPurchase(self, bondPurchID):
        self.bondPurchases.append(bondPurchID)

    def print_data(self):
        """Print report header with account info"""
        acctHolder = self.acctholder_info()
        addrLine = self.acctholder_addr()
        print("-" * 80)
        print(f'{"Stock and Bond Ownership for" : ^80}')
        print(f"{acctHolder : ^80}")
        print(f"{addrLine : ^80}")
        print("-" * 80)

    def return_data(self):
        """Return header with account info"""
        acctHolder = self.acctholder_info()
        addrLine = self.acctholder_addr()
        investor_data = ("-" * 80)
        investor_data = investor_data + ('\n')
        investor_data = investor_data + (f'{"Stock and Bond Ownership for" : ^80}')
        investor_data = investor_data + ('\n')
        investor_data = investor_data + f"{acctHolder : ^80}"
        investor_data = investor_data + ('\n')
        investor_data = investor_data + f"{addrLine : ^80}"
        investor_data = investor_data + ('\n')
        investor_data = investor_data +("-" * 80)
        investor_data = investor_data + ('\n')
        return investor_data

class Purchase:
    """Represents aspects of a transaction."""
    def __init__(self, purchaseID, investorID, symbol, num_shares, purchase_price, purchase_date, current_price, earnings=0, yieldAmt=0, annEarnRate=0, coupon=0):
        """Initialize purchase attributes """
        self.purchaseID = purchaseID
        self.investorID = investorID
        self.symbol = symbol
        self.numShares = num_shares
        self.purchPrice = purchase_price
        self.purchDate = purchase_date
        self.currentPrice = current_price
        self.earnings = earnings
        self.yieldRate = yieldAmt
        self.annEarnRate = annEarnRate
        self.coupon = coupon
        self.closeDate = []
        self.closePrice = []
        self.closeValue = []
        self.closeEarn = []

    def calcEarnings(self) :
        """Calculate the stock gain or loss."""
        try:
            self.earnings = (self.currentPrice - self.purchPrice) * self.numShares
        except TypeError:
            print('Unexpected data type - number expected.')

    def calcYieldRate(self) :
        """Calculate the stock yield rate based on stock earnings & purch price."""
        try:
            self.yieldRate = self.earnings/self.purchPrice
        except TypeError:
            print('Unexpected data type - number expected.')

    def calcAnnEarnRate(self) :
        """Calculate the yearly earnings/loss rate based on earnings."""
        today = date.today()
        try:
            dateDelta = today - self.purchDate
        except TypeError:
            print('Unexpected data type - number expected.')
        dateDelta = dateDelta.days
        self.annEarnRate = (self.yieldRate/dateDelta)*100

    def calcDayValue(self, price):
        """Calculate the stock value based on owned shares and price parameter."""
        try:
            dayValue = self.numShares * price
        except ValueError:
            print("Missing close price.")
        return dayValue

    def calcDayEarn(self, price):
        """Calculate the stock earnings based on owned shares and price parameter."""
        try:
            dayEarn = (price - self.purchPrice) * self.numShares
        except ValueError:
            print("Missing close price.")
        return dayEarn


    def addDailyData(self, date, closePrice, closeValue, closeEarn):
        """Add a closing price, date, value, and earnings to the list attributes."""
        self.closeDate.append(date)
        self.closePrice.append(closePrice)
        self.closeValue.append(closeValue)
        self.closeEarn.append(closeEarn)

    def print_data_stock(self):
        """Print stock detail line."""
        print_string = f"{self.symbol}\t{self.numShares}\t${self.earnings:.2f}\t{self.yieldRate:.2f}\t{self.annEarnRate:.3f}%"
        print(print_string)

    def return_record_stock(self):
        """Print stock detail line."""
        stock_record = f"{self.symbol}\t{self.numShares}\t  ${self.earnings:.2f}\t{self.yieldRate:.2f}\t{self.annEarnRate:.3f}%"
        return stock_record

    def print_data_bond(self):
        """Print bond detail line."""
        #purchDtFormat = self.purchDate.strftime("%m/%d/%Y")
        print_string = f"{self.symbol}\t{self.numShares:>8}\t{self.coupon:>6}\t{self.yieldRate:>5}%\t${self.purchPrice:.2f}\t\t{self.purchDate}\t${self.currentPrice:.2f}"
        print(print_string)

    def return_record_bond(self):
        """Return bond detail line."""
        purchDtFormat = self.purchDate.strftime("%m/%d/%Y")
        bond_record = f"{self.symbol}\t{self.numShares}\t{self.coupon }\t{self.yieldRate}%\t${self.purchPrice:.2f}\t\t{purchDtFormat}\t${self.currentPrice:.2f}"
        return bond_record

class StockHistoryData():
    """Represent closing data for a stock."""
    def __init__(self, stockHistoryID, stockPurchaseID, symbol, date, open, high, low, close, volume):
        self.stockHistoryID = stockHistoryID
        self.stockPurchaseID = stockPurchaseID
        self.symbol = symbol
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

class StockHeader:
    """Report header for stock purchase report section."""
    def print_header(self):
        print(f"{'Stock Holdings' : ^80}")
        print('-' * 80)
        print("Stock\tShare\t\t\t\t   Yearly")
        print("Symbol\t  #\tEarnings/Loss\t Yield\tEarnings/Loss")
        print('-' * 80)

    def return_header(self):
        """Define header for stock purchase section and return."""
        stHeader = f"{'Stock Holdings' : ^80}"
        stHeader = stHeader + '\n'
        stHeader = stHeader + ('-' * 80)
        stHeader = stHeader + '\n'
        stHeader = stHeader + 'Stock\tShare\t\t\t\t   Yearly'
        stHeader = stHeader + '\n'
        stHeader = stHeader + 'Symbol\t  #\tEarnings/Loss\t Yield\tEarnings/Loss'
        stHeader = stHeader + '\n'
        stHeader = stHeader + ('-' * 80)
        stHeader = stHeader + '\n'
        return stHeader

class BondHeader:
    """Report header for bond purchase report section."""
    def print_header(self):
        print('-' * 80)
        print(f"{'Bond Holdings' : ^80}")
        print('-' * 80)
        print("Bond\t\t\t\t\tPurchase\tPurchase\tCurrent")
        print("Symbol\tQuantity\tCoupon\tYield\tPrice\t\tDate\t\tPrice")
        print('-' * 80)

    def return_header(self):
        """Define header for bond purchase section and return."""
        bdHeader = ('-' * 80)
        bdHeader = bdHeader + '\n'
        bdHeader = bdHeader + f"{'Bond Holdings' : ^80}"
        bdHeader = bdHeader + '\n'
        bdHeader = bdHeader + ('-' * 80)
        bdHeader = bdHeader + '\n'
        bdHeader = bdHeader + 'Bond\t\t\t\tPurchase\t\tPurchase\t\tCurrent'
        bdHeader = bdHeader + '\n'
        bdHeader = bdHeader + 'Symbol\tQty\tCoupon\tYield\tPrice\t\tDate\t\tPrice'
        bdHeader = bdHeader + '\n'
        bdHeader = bdHeader + ('-' * 80)
        bdHeader = bdHeader + '\n'
        return bdHeader

class Footer:
    def print_footer(self):
        """Print report footer section."""
        print('-' * 80)

    def return_footer(self):
        """Return report footer section."""
        footer = ('-' * 80)
        footer = footer + '\n'
        return footer
