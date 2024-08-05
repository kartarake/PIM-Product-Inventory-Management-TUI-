def invstockout(con):
    itemdata=modules.shops.fetchitemdata(con)
    changes=modules.shops.fetchchanges(con)
    stockout=0
    initial=0
    listofqty=[]
    for row in changes:
        countofitems=row[1]
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