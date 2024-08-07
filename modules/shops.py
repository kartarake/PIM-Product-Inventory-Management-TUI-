import time, json

import modules.database as database

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

def fetchrole(con, username):
    # To fetch the role of the username
    data = fetchmembers(con)
    
    for i in range(len(data)):
        if data[i][0] == username:
            break
    else:
        raise ValueError("Username not found")

    return data[i][1]

def changerole(con, username, role):
    # To change the role of the username
    data = fetchmembers(con)

    for i in range(len(data)):
        if data[i][0] == username:
            break
    else:
        raise ValueError("Username not found")

    row = (username, role)
    data[i] = row
    database.puttable(con, data)

def newitem(con, itemname, price, desc):
    # To insert a new item data
    record = (itemname, 0, price, desc)
    if not desc == None:
        database.insertrow(con, "itemdata", record)
    else:
        cursor = con.cursor()
        cursor.execute(f"insert into itemdata(itemname, quantity, price) values {record};")
        con.commit()

def additem(con, itemname, count=1):
    # To addd a item into the shop.
    data = fetchitemdata(con)

    for i in range(len(data)):
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

    for i in range(len(data)):
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

def fetchshops(con):
    # To fetch data from shops table
    rdata = database.fetchtable(con, "shops")
    return rdata[0]

def fetchshoplist(con):
    # Returns a list of shop names.
    data = fetchshops(con)
    shoplist = [row[0] for row in data]
    return shoplist

def addshop(con, shopname, multibranch, trackers):
    # To add a new shop to database.

    trackers = json.dumps(trackers)    
    record = (shopname, multibranch, trackers)
    database.insertrow(con, "shops", record)

def fetchbranchlist(con):
    data = fetchshops(con)
    data = json.loads(data[2])
    return data

def setlwshop(con, username, branch):
    data = fetchshops(con)

    trackers = json.loads(data[3])
    trackers[username] = branch
    trackers = json.dumps(trackers)

    cursor = con.cursor()
    cursor.execute(f"""update shops
                   set trackers='{trackers}';""")
    con.commit() 