import time, json

import modules.database as database

def fetchitemdata(con, lwshop):
    # To get the itemdata holding dictionary.
    data = database.fetchtable(con, f"{lwshop}_itemdata")
    return data

def fetchitemlist(con, lwshop):
    # To get the list of all item names.
    return [row[0] for row in fetchitemdata(con, lwshop)]

def fetchitemquantity(con, itemname, lwshop):
    # To get the item quantity in a shop.
    data = fetchitemdata(con, lwshop)

    for row in data:
        if row[0] == itemname:
            break

    return row[1]

def fetchitemprice(con, itemname, lwshop):
    # To get the item price in a shop.
    data = fetchitemdata(con, lwshop)

    for row in data:
        if row[0] == itemname:
            break

    return row[2]

def fetchchanges(con, lwshop):
    # To get the change log in list format.
    data = database.fetchtable(con, f"{lwshop}_changes")
    return data

def fetchmembers(con, lwshop):
    # To get the data of members of that shop.
    data = database.fetchtable(con, f"{lwshop}_members")
    return data

def fetchrole(con, username, lwshop):
    # To fetch the role of the username
    data = fetchmembers(con, lwshop)
    
    for i in range(len(data)):
        if data[i][0] == username:
            break
    else:
        raise ValueError("Username not found")

    return data[i][1]

def changerole(con, username, role, lwshop):
    # To change the role of the username
    data = fetchmembers(con, lwshop)

    for i in range(len(data)):
        if data[i][0] == username:
            break
    else:
        raise ValueError("Username not found")

    row = (username, role)
    data[i] = row
    database.puttable(con, f"{lwshop}_members", data)

def newitem(con, itemname, price, desc, lwshop):
    # To insert a new item data
    record = (itemname, 0, price, desc)
    if not desc == None:
        database.insertrow(con, f"{lwshop}_itemdata", record)
    else:
        cursor = con.cursor()
        cursor.execute(f"insert into {lwshop}_itemdata(itemname, quantity, price) values {record[:-1]};")
        con.commit()

def additem(con, itemname, lwshop, count=1):
    # To addd a item into the shop.
    data = fetchitemdata(con, lwshop)

    for i in range(len(data)):
        if data[i][0] == itemname:
            break

    row = list(data[i])
    row[1] += count
    row = tuple(row)

    data[i] = row
    database.puttable(con, f"{lwshop}_itemdata", data)

    now = time.strftime("%Y%m%d%H%M%S")
    record = (itemname, count, now)
    database.insertrow(con, f"{lwshop}_changes", record)

def removeitem(con, itemname, lwshop, count = 1):
    # To remove a item from the shop.
    data = fetchitemdata(con,lwshop)

    for i in range(len(data)):
        if data[i][0] == itemname:
            break

    row = list(data[i])
    row[1] -= count
    row = tuple(row)

    data[i] = row
    database.puttable(con, f"{lwshop}_itemdata", data)

    now = time.strftime("%Y%m%d%H%M%S")
    record = (itemname, -count, now)
    database.insertrow(con, f"{lwshop}_changes", record)

def addmember(con, member, role, lwshop):
    # To add a member to the shop. role options (owner / admin / clerk)
    record = (member, role)
    database.insertrow(con, f"{lwshop}_members", record)
    
def removemember(con, member, lwshop):
    # To remove a member from the shop.
    where = f"username = {member}"
    database.deleterow(con, f"{lwshop}_members", where)

def checkmemberexists(con, member, lwshop):
    # To check if the member exists in the shop
    data = fetchmembers(con, lwshop)
    for i in range(len(data)):
        if data[i][0] == member:
            return True
    else:
        return False

def fetchmemberpos(con, member, lwshop):
    # To get the index pos of the row of the passed in member
    data = fetchmembers(con, lwshop)
    for i in range(len(data)):
        if data[i][0] == member:
            return i
    else:
        return None

def fetchshops(con):
    # To fetch data from shops table
    rdata = database.fetchtable(con, "shop")
    return rdata[0]

def fetchshoplist(con, lwshop):
    # Returns a list of shop names.
    data = fetchshops(con, lwshop)
    shoplist = [row[0] for row in data]
    return shoplist

def addshop(con, shopname, multibranch, trackers):
    # To add a new shop to database.

    trackers = json.dumps(trackers)    
    record = (shopname, multibranch, trackers)
    database.insertrow(con, "shop", record)

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
    cursor.execute(f"""update shop
                   set trackers='{trackers}';""")
    con.commit() 
