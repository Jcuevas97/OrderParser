import csv

def dataorg(file):
    transbytick = {}
    data = open(file)
    csv_data = csv.reader(data)
    for row in csv_data:
        if row[1] != "Money Movement":
            details = row[2].split(' ')
            odate = row[0]
            fee = row[4]
            if row[1].split(' ')[0] == "Trade":
                ticker = details[2]
                exdate = details[3].lstrip("0")
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
                contracts = details[1]
            elif row[1].split(' ')[0] == "Receive":
                ticker = row[1].split(' ')[2]
                if details[-1] == "expiration.":
                    exdate = details[4].lstrip("0")
                    premium = "$0.00"
                    buysell = "expired"
                    callput = details[5][0]
                    strike = details[6]
                    contracts = details[2]
                elif details[-1] != "exercise" and details[-1] != "assignment":
                    exdate = row[0].split()[0].lstrip("0")
                    premium = row[3]
                    if details[0] == "Bought":
                        buysell = "S"
                    elif details[0] == "Sold":
                        buysell = "B"
                    callput = "Assigned"
                    strike = details[-1]
                    contracts = int(details[3])/100
            if ticker in transbytick:
                if exdate in transbytick[ticker]:
                    if strike in transbytick[ticker][exdate]:
                        if callput in transbytick[ticker][exdate][strike]:
                            if odate > transbytick[ticker][exdate][strike][callput][0][0]:
                                placeholder = transbytick[ticker][exdate][strike][callput][0]
                                transbytick[ticker][exdate][strike][callput] = [[placeholder[0], placeholder[1], placeholder[2], placeholder[3], placeholder[4]+fee, premium, odate]]
                            elif odate == transbytick[ticker][exdate][strike][callput][0][0]:
                                print(ticker)
                                print(transbytick[ticker][exdate][strike][callput][0][0])
                            transbytick[ticker][exdate][strike][callput] += [[odate, buysell, premium, contracts, fee]]
                        else:
                            transbytick[ticker][exdate][strike][callput] = [[odate, buysell, premium, contracts, fee]]
                    else:
                        transbytick[ticker][exdate][strike] = {callput: [[odate, buysell, premium, contracts, fee]]}
                else:
                    transbytick[ticker][exdate] = {strike: {callput: [[odate, buysell, premium, contracts, fee]]}}
            else:
                transbytick[ticker] = {exdate: {strike: {callput: [[odate, buysell, premium, contracts, fee]]}}}



    print("--------------Results-------------------")
    for key in transbytick:
        print("Ticker ================"+key+"-------------------")
        for seckey in transbytick[key]:
            print("    Exp Date =========="+seckey+"----------------------")
            for thirkey in transbytick[key][seckey]:
                print("        Strike ==========" + thirkey + "----------------------")
                for fourthkey in transbytick[key][seckey][thirkey]:
                    print("            Contract ==========" + fourthkey + "----------------------")
                    print("                "+str(transbytick[key][seckey][thirkey][fourthkey]))



def remake(file):
    rerowed = []
    data = open(file)
    csv_data = csv.reader(data)
    for row in csv_data:
        print("------->"+row[1])
        if row[1] != "Money Movement":
            newrow = []
            details = row[2].split(' ')
            print(details)
            ticker = details[2]
            odate = row[0].split(' ')[0]
            exdate = details[3]
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
            contracts = details[1]
            fee = row[4]
        newrow = [ticker,odate,exdate,callput,buysell,strike,premium,contracts,fee]
        rerowed += [newrow]
    return rerowed

def cvsprinter(list):
    with open("remastered.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(list)







def main():
    inp = input("filename:")
    dataorg(inp)

main()