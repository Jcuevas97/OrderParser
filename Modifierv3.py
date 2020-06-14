import copy
import csv
import quickstart
import datetime

class Order:
    """
    A class used to represent an Order

    Attributes
    ----------
    ticker : str
        The ticker for the order
    odate : date str
        The date the order was made
    expdate: date str
        The expiration date of the order
    callput: str
        Either a C or a P representing if the order is a call or a put
    buysell: str
        Either a B or a S representing if the order is a buy or a sell
    strike: float
        The strike price of the order
    premium: float
        The premium received/paid to open the order
    contracts: int
        The quantity of contracts in the order
    fee: float
        Fees paid for the order
    cpremium: float
        The premium received/paid to close the order
    cdate: date str
        The date the order was closed
    real: bool
        Boolean value representing if the order is a proper order or not

    Methods
    -------
    update(o)
        Takes an order object and returns a closed order if it can be closed
        or returns itself it the order cannot be closed
    split()
        Splits an order that contains one or more contracts into a list of
        orders each containing a single contract and then returns that list
    compare(o)
        Compares two orders and returns a bool indicating if they are the
        same order or not
    isclosed()
        Returns a bool indicating if the order is closed or not
    updatecontracts(u)
        Updates the order contract amount with the int u
    updatefee(u)
        Updates the order fee with the float u
    tolist()
        Returns order as a list of the order attributes as strings
    tostring()
        Prints order attributes with labels per attribute
    close(o)
        Closes order with the order passed in as an argument
    merge(o)
        compares and merges two orders
    """

    def __init__(self, row):
        """
        Parameters
        ----------
        row : list
            list of order attributes
        """
        self.ticker = row[0]
        self.odate = row[1]
        self.expdate = row[2]
        self.callput = row[3]
        self.buysell = row[4]
        self.strike = float(row[5])
        self.premium = float(row[6])
        self.contracts = int(row[7])
        self.fee = float(row[8])
        self.cpremium = float(row[9])
        self.cdate = row[10]
        self.broker = row[11]
        self.real = row[12]

    def update(self, o):
        """
        Takes an order object and returns a closed order if it can be closed
        or returns itself it the order cannot be closed

        Parameters
        ----------
        o : Order
            Order object

        Returns
        -------
        Order
            the order being updated
        """

        if (self.broker == o.broker) and (self.expdate == o.expdate) and (self.buysell is not o.buysell) \
                and ((self.callput == o.callput) or
                     ((self.callput == "Assigned") or
                      (self.callput == "Exercised")) or
                     ((o.callput == "Assigned") or
                      (o.callput == "Exercised"))):

            datemax = maxdatefind(self.odate, o.odate)
            if o.odate == datemax:
                self.close(o)
                return self
            elif self.odate == datemax:
                return o.update(self)
        else:
            return self

    def split(self):
        """
        Splits an order that contains one or more contracts into a list of
        orders each containing a single contract and then returns that list

        Returns
        -------
        list
            list of single contract orders
        """
        if self.contracts == 1:
            return [self]
        else:
            splitby = self.contracts
            onefee = self.fee / self.contracts
            self.updatefee(onefee).updatecontracts(1)
            splits = []
            for i in range(splitby):
                splits += [copy.deepcopy(self)]
            return splits

    def compare(self, o):
        """
        Compares two orders

        Parameters
        ----------
        o : Order
            Order object

        Returns
        -------
        bool
            bool indicating if they are the
            same order or not
        """
        return ((self.ticker == o.ticker) and
                (self.odate == o.odate) and
                (self.expdate == o.expdate) and
                (self.callput == o.callput) and
                (self.buysell == o.buysell) and
                (self.strike == o.strike) and
                (self.premium == o.premium) and
                (self.cpremium == o.cpremium) and
                (self.cdate == o.cdate) and
                (self.broker == o.broker))

    def isclosed(self):
        """
        Checks if the order is closed

        Returns
        -------
        bool
            bool indicating if the order is closed
        """
        return self.cdate != ""

    def updatecontracts(self, u):
        """
        Updates contract attribute

        Parameters
        ----------
        u : int
            contract amount to update to

        Returns
        -------
        Order
            Order with updated contract amount
        """
        self.contracts = u
        return self

    def updatefee(self, u):
        """
        Updates fee attribute

        Parameters
        ----------
        u : float
            fee amount to update to

        Returns
        -------
        Order
            Order with updated fee amount
        """
        self.fee = u
        return self

    def tolist(self):
        """
        Returns order as a list of the order attributes

        Returns
        -------
        list
            list of order attributes as strings
        """
        return [str(self.ticker)
            , str(self.odate)
            , str(self.expdate)
            , str(self.callput)
            , str(self.buysell)
            , str(self.strike)
            , str(self.premium)
            , str(self.contracts)
            , str(self.fee)
            , str(self.cpremium)
            , str(self.cdate)
            , self.broker]

    def tostring(self):
        """
        Prints order attributes with labels per attribute

        """
        print("------------------------------------" +
              "\nBroker:    " + self.broker +
              "\nTicker:    " + self.ticker +
              "\nOpen Date: " + self.odate +
              "\nExp. Date: " + self.expdate +
              "\nCall/Put : " + self.callput +
              "\nBuy/Sell : " + self.buysell +
              "\nStrike   : " + self.strike +
              "\nPremium  : " + str(self.premium) +
              "\nContracts: " + str(self.contracts) +
              "\nFee      : " + str(self.fee) +
              "\nClose Price  : " + str(self.cpremium) +
              "\nClose Date: " + self.cdate)

    def close(self, o):
        """
        Closes order with the order passed in as an argument

        Parameters
        ----------
        o : Order
            Order object

        """
        self.fee = float(self.fee) + float(o.fee)
        if (self.callput == "Assigned") or (o.callput == "Assigned") or \
                (self.callput == "Exercised") or (o.callput == "Exercised"):
            self.cpremium = -float(o.premium)
        else:
            self.cpremium = o.premium
        self.cdate = o.odate

    def merge(self, o):
        """
        Merges an order with the order passed in as an argument

        Parameters
        ----------
        o : Order
            Order object

        """

        self.contracts += o.contracts
        self.fee += o.fee


def maxdatefind(s, o):
    ss = s.split('/')
    os = o.split('/')
    date1 = datetime.date(int(ss[2]), int(ss[0]), int(ss[1]))
    date2 = datetime.date(int(os[2]), int(os[0]), int(os[1]))
    return s if date1 >= date2 else o

def dataorg(file, service, sheet=False):
    """
    Takes a file and service and creates a dictionary containing all order information

    Parameters
    ----------
    file : str
        The file location of the order data
    service : str
        A char used to represent where the order data was sourced from
        eg - T is Tastyworks
             R is Robinhood
             G is Google Sheet

    Returns
    -------
    dict
        a nested dictionary where the key is the ticker for the orders with a value of
        a second dictionary where the key is the strike price for the orders
    """

    allorders = {}
    if service == "T" or service == "R":
        data = open(file)
        data_in = csv.reader(data)
    elif service == "G":
        data_in = file
    if sheet != False:
        allorders = dataorg(quickstart.GetOpenOrders(), "G")

    for row in data_in:

        if service == "T":
            currentorder = Order(Tasty2row(row))
        elif service == "R":
            currentorder = Order(Robin2row(row))
        elif service == "G":
            currentorder = Order(Sheet2row(row))
        if not currentorder.real:
            continue
        else:
            if currentorder.ticker in allorders:
                if currentorder.strike in allorders[currentorder.ticker]:
                    # ticklist is all orders with the same ticker and strike as the current order
                    ticklist = allorders[currentorder.ticker][currentorder.strike]
                    updatedlist = []
                    if int(currentorder.contracts) == 1:
                        updatedlist = listcloser(ticklist, currentorder)
                    else:
                        multiorders = currentorder.split()
                        i = 0
                        for orders in multiorders:
                            if i != 0:
                                updatedlist = listcloser(updatedlist, orders)
                            else:
                                updatedlist = listcloser(ticklist, orders)
                                i += 1
                    allorders[currentorder.ticker][currentorder.strike] = updatedlist
                else:
                    # creates an entry in the nested dictionary at strike price of the current order
                    allorders[currentorder.ticker][currentorder.strike] = currentorder.split()
            else:
                # creates an entry in the dictionary for the ticker of the current order
                allorders[currentorder.ticker] = {currentorder.strike: currentorder.split()}
    return allorders


def listcloser(ticklist, currentorder):
    """
    Takes a list of orders and a order and checks if the order can close any
    of the orders in the list. If it can it will close that order and return
    a list of updated orders. if it can't it will add that order to the list
    and return a updated list of orders

    Parameters
    ----------
    ticklist : list
        A list of orders
    currentorder : Order
        A order
    Returns
    -------
    list
        a updated list of orders
    """
    updatedlist = []
    for item in reversed(ticklist):
        tempitem = copy.deepcopy(item).update(currentorder)
        if item.isclosed() != tempitem.isclosed():
            # the order was closed, add all items to list break loop
            updatedlist = updatedlist + [tempitem] + ticklist[:ticklist.index(item)]
            break
        elif (item.isclosed() == tempitem.isclosed()) and ticklist[0] == item:
            # end is reached and nothing changed, add item and current order to list break loop
            updatedlist += [tempitem, currentorder]
            break
        else:
            # end hasn't been reached add the item to list
            updatedlist += [tempitem]
    return updatedlist


def Tasty2row(row):
    """
    Takes a list derived from a single row of Tastywork's Transactions page
    and returns a list formatted to be passed into the Order constructor

    Parameters
    ----------
    row : list
        list of order information

    Returns
    -------
    list
        a list properly formatted for Order constructor
    """
    real = True
    ticker = ""
    cdate = ""
    cpremium = 0.00
    expdate = ""
    callput = ""
    buysell = ""
    strike = 0.00
    premium = 0.00
    contracts = 0
    fee = 0.00
    odate = ""
    # if money movement is the second item in row then the row is not an order
    if row[1] != "Money Movement":
        details = row[2].split(' ')
        odate = row[0].split(' ', 1)[0]
        fee = row[4].strip('$')
        # if the first word in the second item is trade then it is a normal order
        if row[1].split(' ')[0] == "Trade":
            ticker = details[2]
            expdate = details[3].lstrip("0")
            if details[0] == "Bought":
                buysell = "B"
            elif details[0] == "Sold":
                buysell = "S"
            if details[4] == "Call":
                callput = "C"
            elif details[4] == "Put":
                callput = "P"
            strike = details[5]
            premium = details[7]
            contracts = int(details[1])
        # if the first word in the second item is Receive then the order has either
        # been assigned/exercised or expired
        elif row[1].split(' ')[0] == "Receive":
            ticker = row[1].split(' ')[2]
            if details[-1] == "expiration.":
                expdate = details[4].lstrip("0")
                premium = "0.00"
                buysell = "expired"
                callput = details[5][0]
                strike = details[6]
                contracts = int(details[2])
            # Tastyworks has multiple entries for exercising/assignment in this case
            # this entry does not have all the information desired to create a order object
            elif details[-1] == "exercise" or details[-1] == "assignment":
                real = False
            else:
                expdate = row[0].split()[0].lstrip("0")
                premium = details[-1]
                if details[0] == "Buy":
                    buysell = "S"
                    callput = "Exercised"
                elif details[0] == "Sell":
                    buysell = "B"
                    callput = "Assigned"
                strike = details[-1]
                contracts = int(int(details[3]) / 100)
    else:
        real = False

    return [ticker
        , odate
        , expdate
        , callput
        , buysell
        , strike
        , premium
        , contracts
        , fee
        , cpremium
        , cdate
        , "TastyTrade"
        , real]


def Robin2row(row):
    """
    Takes a list derived from a single row of Robinhood's Account statements pdf
    and returns a list formatted to be passed into the Order constructor

    Parameters
    ----------
    row : list
        list of order information

    Returns
    -------
    list
        a list properly formatted for Order constructor
    """
    real = True
    ticker = ""
    cdate = ""
    cpremium = 0.00
    expdate = ""
    callput = ""
    buysell = ""
    strike = 0.00
    premium = 0.00
    contracts = 0
    fee = 0.00
    odate = ""
    # checks if the row is an regular order or if it's a
    # stock purchase/assignment/exercise/expiration
    if len(row) == 1 or (row[-1].replace('.', '', 1).isdigit() and len(row) == 2):
        details = row[0].split(" ")
        # Checks if the row is pending settlement, these trades are not option related
        # so they are set to false
        if "/" in details[7] and "/" in details[6]:
            real = False
        ticker = details[0]
        expdate = details[1].lstrip("0")
        if details[2] == "Call":
            callput = "C"
        elif details[2] == "Put":
            callput = "P"
        strike = details[3].strip("$")
        # When detail[5][0] is not an O then the order is not at expiration
        if details[5][0] != 'O':
            buysell = details[6][0]
            odate = details[7]
            contracts = details[8]
            premium = details[9].strip("$")
        # Robinhood has multiple entries for exercising/assignment in this case
        # this entry does not have all the information desired to create a order object
        elif details[5] == "OASGN" or details[5] == "OEXCS":
            real = False
        elif details[5] == "OEXP":
            odate = details[6]
            if details[7][-1] == "S":
                buysell = "S"
                contracts = details[7].strip('S')
            else:
                buysell = "B"
                contracts = details[7]
            premium = 0
    # Robinhood uses the word Unsolicited when stock is purchased or sold this section checks
    # if they are being purchased or sold due to option assignment or exercise
    elif row[0].split(" ")[-1] == "Unsolicited":
        details = row[1].split(" ")
        if details[5] == "Option":
            ticker = details[4]
            odate = expdate = details[10].lstrip("0")
            strike = premium = details[-2].strip("$")
            if details[9] == "Buy" and details[6] == "Assigned":
                buysell = "B"
                callput = "P"
            elif details[9] == "Buy" and details[6] == "Exercised":
                buysell = "S"
                callput = "C"
            elif details[9] == "Sell" and details[6] == "Assigned":
                buysell = "B"
                callput = "C"
            elif details[9] == "Sell" and details[6] == "Exercised":
                buysell = "S"
                callput = "P"
            contracts = int(int(details[11]) / 100)
        else:
            real = False
    else:
        real = False

    return [ticker
        , odate
        , expdate
        , callput
        , buysell
        , strike
        , premium
        , contracts
        , fee
        , cpremium
        , cdate
        , "Robinhood"
        , real]


def Sheet2row(row):
    rerow = row[0:5] + row[10:13] + row[15:18] + [row[23]] + [True]
    if rerow[9] == "":
        rerow[9] = 0.00
    return rerow


def cvsprinter(allorders, name):
    """
    Takes a dictionary of orders and a file name, then both
    prints each of the orders and adds them to the file

    Parameters
    ----------
    allorders : dict
        a nested dictionary where the key is the ticker for the orders with a value of
        a second dictionary where the key is the strike price for the orders

    """
    with open(name, "w", newline='') as f:
        writer = csv.writer(f)
        for key in allorders:
            for skey in allorders[key]:
                for item in allorders[key][skey]:
                    print(item.tolist())
                    writer.writerow(item.tolist())


def ordercondenser(allorders):
    for ticker in allorders:
        for strike in allorders[ticker]:
            orders = allorders[ticker][strike]
            neworders = []
            if len(orders) == 1:
                continue
            else:
                while len(orders) != 0:
                    current = orders.pop()
                    for i in reversed(orders):
                        if current.compare(i):
                            current.merge(i)
                            orders.remove(i)
                    neworders += [current]
            allorders[ticker][strike] = neworders
    return allorders


def orderlister(dic):
    """
    Takes a dictionary of orders objects and converts the orders into lists
    that are then added to another list which is returned

    Parameters
    ----------
    dic : dict
        a nested dictionary where the key is the ticker for the orders with a value of
        a second dictionary where the key is the strike price for the orders

    Returns
    -------
    list
        a list of orders converted to lists
    """
    relisted = []
    for key in dic:
        for skey in dic[key]:
            for item in dic[key][skey]:
                relisted += [item.tolist()]
    return relisted


if __name__ == '__main__':
    inp = "C:\\Users\\johnn\\Desktop\\Finance Updater\\MoreTaste.csv"
    # inp = "A:\\Programing\\Finance Updater\\Tests\\RTest 5.csv"
    # out = input("Enter filename for export:   ")
    cvsprinter(ordercondenser(dataorg(inp, "T", False)), "outT.csv")
