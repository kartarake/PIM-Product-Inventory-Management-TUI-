from modules import shops
from modules.boxify import boxify

def days(timestamp):
    days = int(timestamp[0:4])*365 + int(timestamp[5:7])*30 + int(timestamp[8:10])
    return days

def timeperiod(con, lwshop, timestamp):
    # to calculate time period from the given stamp
    start_time = days(timestamp)
    itemlist = shops.fetchitemlist(con, lwshop)

    data = shops.fetchchanges(con, lwshop)
    mapping = {}
    for item in itemlist:
        mapping[item] = []
    for row in data:
        mapping[row[0]].append(row)
    end_time_map = {}
    for key in mapping:
        end_time_map[key] = days(mapping[key][-1][2])
    timeperiod_map = {}
    for key in end_time_map:
        timeperiod_map[key] = end_time_map[key] - start_time

    return timeperiod_map   


def invturnover(con, lwshop): # ERROR
    itemdata=shops.fetchitemdata(con, lwshop)
    changes=shops.fetchchanges(con, lwshop)
    list1=[]
    listofquantity=[]
    for transc in changes:
        count=transc[1]
        itemname=transc[0]
        if count<0:
            for row in itemdata:
                if itemname in row:
                    break
            price=count*row[2]
            list1.append(price)
    cost=sum(list1)
    list2=[]
    for total in itemdata:
        quantity=total[1]
        list2.append(quantity)
    numofitems=len(itemdata)
    totalitems=sum(listofquantity)
    averageinv=totalitems/numofitems
    turnover=cost/averageinv
    return turnover


def invstockout(con, lwshop): # ERROR
    itemdata=shops.fetchitemdata(con, lwshop)
    changes=shops.fetchchanges(con, lwshop)
    stockout=0
    initial=0
    listofqty=[]
    for rows in changes:
        countofitems=rows[1]
        initial=initial+countofitems
        if initial==0:
            stockout+=1
        print('Number of stockouts : ',stockout)
    for total in itemdata:
        quantity=total[1]
        listofqty.append(quantity)
    totalitems=sum(listofqty)
    stockoutrate=totalitems/stockout
    return stockoutrate


def ABCanalysis(con, lwshop): # ERROR
    timestamp = int(input("Enter timestamp:"))
    timeperiod_map = timeperiod(con,lwshop,timestamp)
    A=[]
    B=[]
    C=[]
    for i in timeperiod_map:
        stock = shops.fetchitemquantity(con,i,lwshop)
        demand = timeperiod_map[i]
        megconstant = stock/demand
        if megconstant == 1:
            A.append(i)
        elif megconstant<1:
            B.append(i)
        elif megconstant>1:
            C.append(i)

    if len(A)!=0:
        print("'A' items:",A)
        print(len(A),"is properly maintained in your inventory")
    else:
        print("No item in your inventory is properly managed")
    
    if len(B)!=0:
        print("'B' items:",B)
        print("These are the items that has high demand and low stock")
    else:
        pass
    
    if len(C)!=0:
        print("'C' items:",C)
        print("These are the items that has low demand and high stock")
    else:
        pass