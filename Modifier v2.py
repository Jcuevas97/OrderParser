import csv

class Order:
    def __init__(self, row):
        self.real = True
        self.cdate = ""
        self.cpremium = ""
        self.expdate = ""
        self.callput = ""
        self.buysell = ""
        self.strike = ""
        self.premium = ""
        self.contracts = ""
        if row[1] != "Money Movement":
            details = row[2].split(' ')
            self.odate = row[0]
            self.fee = row[4].strip('$')
            if row[1].split(' ')[0] == "Trade":
                self.ticker = details[2]
                self.expdate = details[3].lstrip("0")
                if details[0] == "Bought":
                    self.buysell = "B"
                elif details[0] == "Sold":
                    self.buysell = "S"
                if details[4] == "Call":
                    self.callput = "C"
                elif details[4] == "Put":
                    self.callput = "P"
                self.strike = details[5]
                self.premium = details[7]
                self.contracts = details[1]
            elif row[1].split(' ')[0] == "Receive":
                self.ticker = row[1].split(' ')[2]
                if details[-1] == "expiration.":
                    self.expdate = details[4].lstrip("0")
                    self.premium = "0.00"
                    self.buysell = "expired"
                    self.callput = details[5][0]
                    self.strike = details[6]
                    self.contracts = details[2]
                elif details[-1] == "exercise" or details[-1] == "assignment":
                    self.real = False
                else:
                    self.expdate = row[0].split()[0].lstrip("0")
                    self.premium = details[-1]
                    if details[0] == "Buy":
                        self.buysell = "S"
                        self.callput = "Exercised"
                    elif details[0] == "Sell":
                        self.buysell = "B"
                        self.callput = "Assigned"
                    self.strike = details[-1]
                    self.contracts = int(details[3]) / 100
        else:
            self.real = False


    def update(self, o):
        if (self.expdate == o.expdate) and (self.buysell == o.buysell) and (self.premium == o.premium):
            self.contracts = int(self.contracts) + int(o.contracts)
            self.fee = float(self.fee) + float(o.fee)
            return self
        elif (self.expdate == o.expdate) and (self.buysell is not o.buysell) and ((self.callput == o.callput) or
                                                                                  ((self.callput == "Assigned") or
                                                                                   (self.callput == "Exercised")) or
                                                                                  ((o.callput == "Assigned") or
                                                                                   (o.callput == "Exercised"))):

            tempmax = max(self.odate, o.odate)
            if o.odate == tempmax:
                if self.contracts == o.contracts:
                    self.fee = float(self.fee) + float(o.fee)
                    if (self.callput == "Assigned") or (o.callput == "Assigned"):
                        self.cpremium = -float(o.premium)
                    elif (self.callput == "Exercised") or (o.callput == "Exercised"):
                        self.cpremium = -float(o.premium)
                    else:
                        self.cpremium = o.premium
                    self.cdate = tempmax
                    return self
                elif self.contracts >= o.contracts:
                    # split self order in 2 one with o contract amount and second with rest
                    # close first order
                    # return closed order and second order
                    self.fee = float(self.fee) + float(o.fee)
                    if (self.callput == "Assigned") or (o.callput == "Assigned"):
                        self.cpremium = -float(o.premium)
                    elif (self.callput == "Exercised") or (o.callput == "Exercised"):
                        self.cpremium = -float(o.premium)
                    else:
                        self.cpremium = o.premium
                    self.cdate = tempmax
                    return self
                elif self.contracts >= o.contracts:
                    # split o order in 2 one with self contract amount and second with rest
                    # close first order
                    # return closed order and second order
                    self.fee = float(self.fee) + float(o.fee)
                    if (self.callput == "Assigned") or (o.callput == "Assigned"):
                        self.cpremium = -float(o.premium)
                    elif (self.callput == "Exercised") or (o.callput == "Exercised"):
                        self.cpremium = -float(o.premium)
                    else:
                        self.cpremium = o.premium
                    self.cdate = tempmax
                    return self
            elif self.odate == tempmax:
                return o.update(self)
        else:
            return [self, o]


    def tolist(self):
       return [str(self.ticker)
              ,str(self.odate)
              ,str(self.expdate)
              ,str(self.callput)
              ,str(self.buysell)
              ,str(self.strike)
              ,str(self.premium)
              ,str(self.contracts)
              ,str(self.fee)
              ,str(self.cpremium)
              ,str(self.cdate)]


    def tostring(self):
        print("------------------------------------" +
              "\nTicker:    " + self.ticker +
              "\nOpen Date: " + self.odate +
              "\nExp. Date: " + self.expdate +
              "\nCall/Put : " + self.callput +
              "\nBuy/Sell : " + self.buysell +
              "\nStrike   : " + self.strike +
              "\nPremium  : " + self.premium +
              "\nContracts: " + str(self.contracts) +
              "\nFee      : " + str(self.fee) +
              "\nClose Price  : " + str(self.cpremium) +
              "\nClose Date: " + str(self.cdate))

def dataorg(file):
    allorders = {}
    data = open(file)
    csv_data = csv.reader(data)
    for row in csv_data:
        currentorder = Order(row)
        if not currentorder.real:
            continue
        else:
            if currentorder.ticker in allorders:
                if currentorder.strike in allorders[currentorder.ticker]:
                    ticklist = allorders[currentorder.ticker][currentorder.strike]
                    updatedlist = []
                    for item in ticklist:
                        tempcontract = item.update(currentorder)
                        if not isinstance(tempcontract, Order):
                            updatedlist += tempcontract
                        else:
                            updatedlist += [tempcontract]
                    allorders[currentorder.ticker][currentorder.strike] = updatedlist
                else:
                    allorders[currentorder.ticker][currentorder.strike] = [currentorder]
            else:
                allorders[currentorder.ticker] = {currentorder.strike: [currentorder]}
    return allorders


def cvsprinter(allorders,name):
    with open(name, "w", newline='') as f:
        writer = csv.writer(f)
        for key in allorders:
            for skey in allorders[key]:
                for item in allorders[key][skey]:
                    print(item.tolist())
                    writer.writerow(item.tolist())


def main():
    inp = input("Enter file to be parsed")
    out = input("Enter filename for export")
    cvsprinter(dataorg(inp), out)

main()