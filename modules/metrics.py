from modules import shops
from modules.boxify import boxify

import math

# TIMESTAMP FORMAT
# YYYY-MM-DD
# 0123456789

def days(timestamp):
    years_to_days = (int(timestamp[0:4])-1) * 365
    months_to_days = (int(timestamp[5:7])-1) * 30
    days_convertion = int(timestamp[8:10])
    total_days = years_to_days + months_to_days + days_convertion
    return total_days

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


"""def invturnover(con, lwshop): # ERROR
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
    return turnover"""
def issameyear(year, timestamp):
    return int(timestamp[0:4]) == year

def calc_inv_till(con, lwshop, index):
    changes = shops.fetchchanges(con, lwshop)

    inventory = 0
    for i in range(index):
        item = changes[i][0]
        itemprice = shops.fetchitemprice(con, item, lwshop)
        change = changes[i][1]
        inventory += change * itemprice
    return inventory
    

def averageinv(con, lwshop, year):
    changes = shops.fetchchanges(con, lwshop)
    itemdata = shops.fetchitemdata(con, lwshop)

    for i in list(range(len(changes))):
        if issameyear(year, changes[i][2]):
            first_change_rowpos = i + 1
            break
    else:
        return None
    
    for i in list(range(len(changes)))[::-1]:
        if issameyear(year, changes[i][2]):
            final_change_rowpos = i + 1
            break
    else:
        return None
    
    first_inventory = 0
    for i in range(first_change_rowpos):
        item = changes[i][0]
        itemprice = shops.fetchitemprice(con, item, lwshop)
        change = changes[i][1]
        first_inventory += change * itemprice

    final_inventory = 0
    for i in range(final_change_rowpos):
        item = changes[i][0]
        itemprice = shops.fetchitemprice(con, item, lwshop)
        change = changes[i][1]
        final_inventory += change * itemprice

    average_inventory = final_inventory - first_inventory / 2
    return average_inventory

def invturnover(con, lwshop):
    pass


def invstockout(con, lwshop):
    # To calculate the stockout rate
    itemdata = shops.fetchitemdata(con, lwshop)

    stockout = 0
    total = len(itemdata)
    if total == 0:
        return None

    for row in itemdata:
        if row[1] == 0:
            stockout += 1
    
    stockoutrate = stockout / total * 100
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