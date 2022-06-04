"""
   Author: Linda Ziembko ICT 4370
   Date Created: June 5, 2022
   Functionality:
                  Week 10 Assignment
                  Create invstor account object
                  Use pandas to create stock & bond objects from csv data files
                  Use pandas to create stock history object list from json file
                  Add stock history data attributes to stock data objects
                  Write investor, stock, bond & stock history objects to sqlite tables
                  Print report from tables
                  Write report data to file
                  Use matplotlib to chart closing value for each stock over period owned
                  Save chart to file and display to screen
                  Use matplotlib to chart earnings value for each stock over period owned
                  Save chart to file and display to screen
                  Use pandas w/matplotlib to chart acct earnings of all stocks/period owned
                  Save chart to file and display to screen
"""
#import sqlite, pandas, datetime and date function from datatime module
import sqlite3
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from datetime import date
from ZiembkoL_StockClasses import *

class main():
    """Creates investor acccount, reads stock & bonds from dataframe, prints reports & writes to file"""
    #Load the stock csv to a pandas dataframe
    stock_file = 'Lesson6_Data_Stocks.csv'
    try:
        df = pd.read_csv(stock_file)
    except FileNotFoundError:
        print(f"The file {stock_file} cannot be found.")
    else:
        df['PURCHASE_DATE'] = pd.to_datetime(df['PURCHASE_DATE']).dt.date
        #print(df)
        #print(df.dtypes)

    #Load the bond csv to a pandas dataframe
    bond_file = 'Lesson6_Data_Bonds.csv'
    try:
        dfB = pd.read_csv(bond_file)
    except FileNotFoundError:
        print(f"The file {bond_file} cannot be found.")
    else:
        dfB['PURCHASE_DATE'] = pd.to_datetime(dfB['PURCHASE_DATE']).dt.date
        #print(dfB)
        #print(dfB.dtypes)

    #Load the stock history data json to a pandas dataframe
    stock_history_file = 'AllStocks.json'
    try:
        dfC = pd.read_json(stock_history_file)
    except FileNotFoundError:
        print(f"The file {stock_history_file} cannot be found.")
    else:
        dfC['Date'] = pd.to_datetime(dfC['Date']).dt.date
        #print(dfC)
        #print(dfC.dtypes)


    #Create investor account account object
    acct1234 = Investor('INV00001','1234SMITH','bob', 'smith', '123 main st', 'denver', 'co', '80208', '303-555-1212')

    #Create list for stock purchaes
    acct1234_stPurchases = []
    #Read dataframe rows, create stock purchase objects from classes and add to list
    for idx, row in df.iterrows():
        newStockPurch = Purchase('SP' + str(idx),
        '1234SMITH',
        row['SYMBOL'],
        row['NO_SHARES'],
        row['PURCHASE_PRICE'],
        row['PURCHASE_DATE'],
        row['CURRENT_VALUE'])
        acct1234_stPurchases.append(newStockPurch)

    #Add stock purchases to invetor account list
    for stock in acct1234_stPurchases:
        acct1234.add_stockPurchase(stock.purchaseID)

    #Create list for bond purchaes
    acct1234_bondPurchases = []
    #Read dataframe rows, create bond purchase objects from classes and add to list
    for idx, row in dfB.iterrows():
        newBondPurch = Purchase('BP' + str(idx),
        '1234SMITH',
        row['SYMBOL'],
        row['NO_SHARES'],
        row['PURCHASE_PRICE'],
        row['PURCHASE_DATE'],
        row['CURRENT_VALUE'],
        0,
        row['Yield'],
        0,
        row['Coupon'])
        acct1234_bondPurchases.append(newBondPurch)

    #Add bond purchases to invetor account list
    for bond in acct1234_bondPurchases:
        acct1234.add_bondPurchase(bond.purchaseID)

    #Create list for stock history objects.
    acct1234_stockHistory = []
    for stock in acct1234_stPurchases:
        #For each stock in the list, read a row from the stock data dataframe
        for idx, row in dfC.iterrows():
            #Test if current symbol from json file is same as current stock in list
            if row['Symbol'] == stock.symbol:
                #Add number of shares to dataframe
                dfC['Num Shares'] = stock.numShares
                dfC['Purchase Price'] = stock.purchPrice
                #Calc daily value and daily earnings then add to stock object
                closingStockValue = stock.calcDayValue(row['Close'])
                closingStockEarn = stock.calcDayEarn(row['Close'])
                stock.addDailyData(row['Date'], row['Close'], closingStockValue, closingStockEarn)
                #Build new object in the history List for import into sqlite table
                newStockHistory = StockHistoryData('SH' + str(idx),
                stock.purchaseID,
                row['Symbol'],
                row['Date'],
                row['Open'],
                row['High'],
                row['Low'],
                row['Close'],
                row['Volume'])
                acct1234_stockHistory.append(newStockHistory)

    #Write data to data tables
    #Function to create tables
    def create_tables(cursor):
        sql_create_investors_table = """CREATE TABLE IF NOT EXISTS investors (
        investorID text PRIMARY KEY,
        investorAcctNum text NOT NULL,
        investorFName text NOT NULL ,
        investorLname text NOT NULL,
        investorAddr text NOT NULL,
        investorCity text NOT NULL,
        investorState text NOT NULL,
        investorZip text NOT NULL,
        investorPhone text NOT NULL );"""

        sql_create_stocks_table = """CREATE TABLE IF NOT EXISTS stocks (
        stockID text PRIMARY KEY,
        investorID text NOT NULL,
        stockSymbol text NOT NULL,
        stockShareNum integer NOT NULL,
        stockPurchPrice real NOT NULL,
        stockPurchDate date NOT NULL,
        stockCurPrice real NOT NULL,
        stockEarnings real NOT NULL,
        stockYieldRate real NOT NULL,
        stockAnnEarnRate real NOT NULL,
        stockCoupon real NOT NULL );"""

        sql_create_bonds_table = """CREATE TABLE IF NOT EXISTS bonds (
        bondID text PRIMARY KEY,
        investorID text NOT NULL,
        bondSymbol text NOT NULL,
        bondShareNum integer NOT NULL,
        bondPurchPrice real NOT NULL,
        bondPurchDate text NOT NULL,
        bondCurPrice real NOT NULL,
        bondEarnings real NOT NULL,
        bondYieldRate real NOT NULL,
        bondAnnEarnRate real NOT NULL,
        bondCoupon real NOT NULL );"""

        sql_create_stockHistory_table = """CREATE TABLE IF NOT EXISTS stockHistory (
        stockHistoryID text PRIMARY KEY,
        stockID text NOT NULL,
        symbol text NOT NULL,
        date text NOT NULL,
        open text NOT NULL,
        high text NOT NULL,
        low text NOT NULL,
        close real NOT NULL,
        volume integer NOT NULL );"""

        #Execute table create functions
        cursor.execute(sql_create_investors_table)
        print("Investor table created.")
        cursor.execute(sql_create_stocks_table)
        print("Stocks table created.")
        cursor.execute(sql_create_bonds_table)
        print("Bonds table created.")
        cursor.execute(sql_create_stockHistory_table)
        print("Stock History table created.")
        print("Tables created succcessfully.\n\n")

    #Fucntion to write data to investor table
    def write_data_investor(cursor, investorAcct):
        sql_insert_investor = "INSERT INTO investors VALUES('" + investorAcct.investorID + "'"
        sql_insert_investor = sql_insert_investor + ", '" + investorAcct.acctNumber + "'"
        sql_insert_investor = sql_insert_investor + ", '" + investorAcct.firstName + "'"
        sql_insert_investor = sql_insert_investor + ", '" + investorAcct.lastName + "'"
        sql_insert_investor = sql_insert_investor + ", '" + investorAcct.address + "'"
        sql_insert_investor = sql_insert_investor + ", '" + investorAcct.city + "'"
        sql_insert_investor = sql_insert_investor + ", '" + investorAcct.state + "'"
        sql_insert_investor = sql_insert_investor + ", '" + investorAcct.zipCode + "'"
        sql_insert_investor = sql_insert_investor + ", '" + investorAcct.phoneNumber + "');"

        #Execute write to investor table
        print(f"Investor account: {sql_insert_investor}")
        cursor.execute(sql_insert_investor)
        print(f"Inserted: {investorAcct.investorID} {investorAcct.acctNumber}")

    #Fucntion to write data to stocks table
    def write_data_stocks(cursor, stock_list):
        for stock in stock_list:
            stock.calcEarnings()
            stock.calcYieldRate()
            stock.calcAnnEarnRate()
            sql_insert_stock = "INSERT INTO stocks VALUES('" + stock.purchaseID + "'"
            sql_insert_stock = sql_insert_stock + ", '" + stock.investorID + "'"
            sql_insert_stock = sql_insert_stock + ", '" + stock.symbol + "'"
            sql_insert_stock = sql_insert_stock + ", " + str(stock.numShares)
            sql_insert_stock = sql_insert_stock + ", " + str(stock.purchPrice)
            sql_insert_stock = sql_insert_stock + ", " + str(stock.purchDate)
            sql_insert_stock = sql_insert_stock + ", " + str(stock.currentPrice)
            sql_insert_stock = sql_insert_stock + ", " + str(stock.earnings)
            sql_insert_stock = sql_insert_stock + ", " + str(stock.yieldRate)
            sql_insert_stock = sql_insert_stock + ", " + str(stock.annEarnRate)
            sql_insert_stock = sql_insert_stock + ", " + str(stock.coupon)
            sql_insert_stock = sql_insert_stock + ");"

            #Execute write to stock table
            print(sql_insert_stock)
            cursor.execute(sql_insert_stock)
            print(f"Inserted: {stock.symbol}")

    #Fucntion to write data to bonds table
    def write_data_bonds(cursor, bond_list):
        for bond in bond_list:
            sql_insert_bond = "INSERT INTO bonds VALUES('" + bond.purchaseID + "'"
            sql_insert_bond = sql_insert_bond + ", '" + bond.investorID + "'"
            sql_insert_bond = sql_insert_bond + ", '" + bond.symbol + "'"
            sql_insert_bond = sql_insert_bond + ", " + str(bond.numShares)
            sql_insert_bond = sql_insert_bond + ", " + str(bond.purchPrice)
            sql_insert_bond = sql_insert_bond + ", '" + str(bond.purchDate) + "'"
            sql_insert_bond = sql_insert_bond + ", " + str(bond.currentPrice)
            sql_insert_bond = sql_insert_bond + ", " + str(bond.earnings)
            sql_insert_bond = sql_insert_bond + ", " + str(bond.yieldRate)
            sql_insert_bond = sql_insert_bond + ", " + str(bond.annEarnRate)
            sql_insert_bond = sql_insert_bond + ", " + str(bond.coupon)
            sql_insert_bond = sql_insert_bond + ");"

            #Execute write to bond table
            print(sql_insert_bond)
            cursor.execute(sql_insert_bond)
            print(f"Inserted: {bond.symbol}")

    #Fucntion to write data to stock history table
    def write_data_stockHistory(cursor, stockHistory_list):
        for history in stockHistory_list:
            sql_insert_history = "INSERT INTO stockHistory VALUES('" + history.stockHistoryID + "'"
            sql_insert_history = sql_insert_history + ", '" + history.stockPurchaseID + "'"
            sql_insert_history = sql_insert_history + ", '" + history.symbol + "'"
            sql_insert_history = sql_insert_history + ", '" + str(history.date) + "'"
            sql_insert_history = sql_insert_history + ", '" + str(history.open) + "'"
            sql_insert_history = sql_insert_history + ", '" + str(history.high) + "'"
            sql_insert_history = sql_insert_history + ", '" + str(history.low) + "'"
            sql_insert_history = sql_insert_history + ", " + str(history.close)
            sql_insert_history = sql_insert_history + ", " + str(history.volume)
            sql_insert_history = sql_insert_history + ");"

            #Execute write to stock history table
            cursor.execute(sql_insert_history)


    #Fucntion to read data from investor table
    def read_investors(cursor):
        sql_investor_select = "SELECT * FROM INVESTORS;"
        db_investors = []
        for record in cursor.execute(sql_investor_select):
            new_db_investor = Investor(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8])
            db_investors.append(new_db_investor)
        return db_investors

    #Fucntion to read data from stocks table
    def read_stocks(cursor):
        sql_stock_select = "SELECT * FROM STOCKS;"
        db_stocks = []
        for record in cursor.execute(sql_stock_select):
            new_db_stock = Purchase(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10])
            db_stocks.append(new_db_stock)
        return db_stocks

    #Fucntion to read data from bonds table
    def read_bonds(cursor):
        sql_bond_select = "SELECT * FROM BONDS;"
        db_bonds = []
        for record in cursor.execute(sql_bond_select):
            new_db_bond = Purchase(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10] )
            db_bonds.append(new_db_bond)
        return db_bonds

    #Set path for database file & define cursor
    dbPath = r'ZiembkoFinal.db'
    connection = sqlite3.connect(dbPath)
    cursor = connection.cursor()
    #Create tables and write data
    create_tables(cursor)
    write_data_investor(cursor, acct1234)
    write_data_stocks(cursor, acct1234_stPurchases)
    write_data_bonds(cursor, acct1234_bondPurchases)
    write_data_stockHistory(cursor, acct1234_stockHistory)

    #Read investors from table and print report section
    db_investors = read_investors(cursor)
    for investor in db_investors:
        investor.print_data()

    #Print stock header and stock earning details
    header = StockHeader()
    header.print_header()

    #Read stocks from table and print report section
    db_stocks = read_stocks(cursor)
    for stock in db_stocks:
        stock.print_data_stock()

    #Print bond header and bond holdings details
    header = BondHeader()
    header.print_header()

    #Read bonds from table and print report section
    db_bonds = read_bonds(cursor)
    for bond in db_bonds:
        bond.print_data_bond()

    #Print footer line
    footer = Footer()
    footer.print_footer()

    connection.close()

    #Write acct report data to file
    try:
        output_file = open(r'ZiembkoL_output.txt','w')
    except:
        print("Error opening output file.")
    #Write account info header to file
    output_file.write(acct1234.return_data())
    #Write stock header to file
    stHeader = StockHeader()
    output_file.write(stHeader.return_header())
    #Write stock detail lines to file
    for st_purchase in acct1234_stPurchases:
        output_file.write(st_purchase.return_record_stock() + '\n')
    #Write bond header to file
    bdHeader = BondHeader()
    output_file.write(bdHeader.return_header())
    #Write bond detail lines to file
    for bd_purchase in acct1234_bondPurchases:
        output_file.write(bd_purchase.return_record_bond() + '\n')
    #Write footer line to file
    footer = Footer()
    output_file.write(footer.return_footer())
    output_file.close()

    #CHART 1 - Stock value at close by stock
    #Create the stock value chart
    fig, ax = plt.subplots(figsize=(15,7))
    for stock in acct1234_stPurchases:
        stockValues = stock.closeValue
        dates = stock.closeDate
        name = stock.symbol
        plt.plot_date(dates, stockValues, linestyle='solid', marker='None', label=name)
    #Add legends and labels to chart, format axis values and add chart title
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Closing Value (US Dollars)')
    ax.yaxis.set_major_formatter('${x:,.0f}')
    plt.title("Closing Value of Shares Owned by Stock for " + acct1234.firstName.title() + " " + acct1234.lastName.title())
    plt.savefig('ZiembkoL_simplePlot.png')
    plt.show()

    #CHART 2 - Stock earnings at close by stock
    #Create the stock earnings chart
    fig, ax = plt.subplots(figsize=(15,7))
    for stock in acct1234_stPurchases:
        stockEarningsCl = stock.closeEarn
        dates = stock.closeDate
        name = stock.symbol
        plt.plot_date(dates, stockEarningsCl, linestyle='solid', marker='None', label=name)
    #Add legends and labels to chart, format axis values and add chart title
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Earnings (US Dollars)')
    ax.yaxis.set_major_formatter('${x:,.0f}')
    plt.title("Earnings at Close by Stock and Shares Owned for " + acct1234.firstName.title() + " " + acct1234.lastName.title())
    plt.savefig('ZiembkoL_stockEarningsPlot.png')
    plt.show()


    #CHART 3 - Account Earnings by Date
    #Add an Earnings Column to the dataframe and calc earnings - for plotting
    dfC['Earnings'] = (dfC['Close'] - dfC['Purchase Price']) * dfC['Num Shares']
    dfC.groupby(['Date'])['Earnings'].sum().reset_index()
    #Create a dataframe with the sum of earnings by date
    earnings_df = dfC.groupby(['Date'])['Earnings'].sum().reset_index()

    #Find the max, min, start and end earnings and associated dates to label on chart
    max_earn_date = earnings_df.loc[earnings_df['Earnings'].idxmax(), 'Date'].strftime("%b %d, %Y")
    max_earnings = round(earnings_df.loc[earnings_df['Earnings'].idxmax(), 'Earnings'],0)
    min_earn_date = earnings_df.loc[earnings_df['Earnings'].idxmin(), 'Date'].strftime("%b %d, %Y")
    min_earnings = round(earnings_df.loc[earnings_df['Earnings'].idxmin(), 'Earnings'],0)
    start_earn_date = earnings_df.iloc[0, 0].strftime("%b %d, %Y")
    start_earnings = round(earnings_df.iloc[0, 1],0)
    end_earn_date = earnings_df.iloc[-1, 0].strftime("%b %d, %Y")
    end_earnings = round(earnings_df.iloc[-1, 1],0)

    #Style the plot labels
    font = {
        'color':  'saddlebrown',
        'weight': 'bold',
        'size': 8
        }

    box = {'facecolor': 'none',
       'edgecolor': 'black'
      }
    #Set the variable for the chart title
    set_title = f"Total Account Earnings at Close for {acct1234.firstName.title()} {acct1234.lastName.title()}"
    set_title = f"{set_title}\n for the Period {start_earn_date} through {end_earn_date}"
    #Plot the chart
    ax = dfC.groupby(['Date']).agg({'Earnings':['sum']}).plot(kind='line', legend=False, grid=True, figsize=(15,7))
    #Add lables to the chart for high, low, start and end with earnings and date
    plt.text(max_earn_date, max_earnings,'High: $' + str("{:,.0f}".format(max_earnings)) + ' on ' + str(max_earn_date), fontdict=font, bbox=box)
    plt.text(min_earn_date, min_earnings,'Low: $' + str("{:,.0f}".format(min_earnings)) + ' on ' + str(min_earn_date), fontdict=font, bbox=box)
    plt.text(start_earn_date, start_earnings,'Start: $' + str("{:,.0f}".format(start_earnings)) + ' on ' + str(start_earn_date), fontdict=font, bbox=box)
    plt.text(end_earn_date, end_earnings,'End: $' + str("{:,.0f}".format(end_earnings)) + ' on ' + str(end_earn_date), fontdict=font, bbox=box)
    #Add and format axis values, add axis labels, and add chart title
    ax.yaxis.set_major_formatter('${x:,.0f}')
    plt.ylabel('Earnings (US Dollars)')
    plt.title(set_title)
    plt.savefig('ZiembkoL_acctEarningsPlot.png')
    plt.show()

#Execute the main class for creating classes and loading data from external files
if __name__ == '__main__':
    main()
