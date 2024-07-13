import time
import database

def fetchitemdata(con):
    # To get the itemdata holding dictionary.
    data = database.fetchtable(con, "itemdata")
    return data

def fetchitemlist(con):
    # To get the list of all item names.
    return [row[0] for row in fetchitemdata(con)]

def fetchitemquantity(con, itemname):
    # To get the item quantity in a shop.
    data = fetchitemdata(con)

    for row in data:
        if row[0] == itemname:
            break

    return row[1]

def fetchchanges(con):
    # To get the change log in list format.
    data = database.fetchtable(con, "changes")
    return data

def fetchmembers(con):
    # To get the data of members of that shop.
    data = database.fetchtable(con, "members")
    return data

def newitem(con, itemname, price, desc):
    # To insert a new item data
    record = (itemname, 0, price, desc)
    database.insertrow(con, "itemdata", record)

def additem(con, itemname, count=1):
    # To addd a item into the shop.
    data = fetchitemdata(con)

    for i in len(data):
        if data[i][0] == itemname:
            break

    row = list(data[i])
    row[1] += count
    row = tuple(row)

    data[i] = row
    database.puttable(con, "itemdata", data)

    now = time.strftime("%Y%m%d%H%M%S")
    record = (itemname, count, now)
    database.insertrow(con, "changes", record)

def removeitem(con, itemname, count = 1):
    # To remove a item from the shop.
    data = fetchitemdata(con)

    for i in len(data):
        if data[i][0] == itemname:
            break

    row = list(data[i])
    row[1] -= count
    row = tuple(row)

    data[i] = row
    database.puttable(con, "itemdata", data)

    now = time.strftime("%Y%m%d%H%M%S")
    record = (itemname, -count, now)
    database.insertrow(con, "changes", record)

def addmember(con, member, role):
    # To add a member to the shop. role options (owner / admin / clerk)
    record = (member, role)
    database.insertrow(con, "members", record)
    
def removemember(con, member):
    # To remove a member from the shop.
    where = f"username = {member}"
    database.deleterow(con, "members", where)