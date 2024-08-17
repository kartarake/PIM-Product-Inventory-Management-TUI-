import shops

def totaltimeperiod(con, lwshop):
    data = shops.fetchchanges(con, lwshop)
    firstrow = data[0]
    lastrow = data[-1]

    start = str(firstrow[2])
    end = str(lastrow[2])

    start = int(start[0:4])*365 + int(start[5:7])*30 + int(start[8:10])
    end = int(end[0:4])*365 + int(end[5:7])*30 + int(end[8:10])

    timeperiod = end - start
    return timeperiod

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

def invturnover(con):
    itemdata=shops.fetchitemdata(con)
    changes=shops.fetchchanges(con)
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


def invstockout(con):
    itemdata=shops.fetchitemdata(con)
    changes=shops.fetchchanges(con)
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
