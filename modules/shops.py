import time

def newshop(db, shopname):
    # To create an empty new shop use this by passing shopname as arg.
    data = {"quantity":{}, "changes":[], "members":{}}

    db.changedoc("shop")
    db.data[shopname] = data
    db.savedoc()

def fetchshopdata(db, shopname):
    # To get the whole data of a shop, use this by passing shopname as arg.
    db.changedoc("shop")
    return db.data[shopname]

def fetchquantity(db, shopname):
    # To get the quantity holding dictionary.
    db.changedoc("shop")
    return db.data[shopname]["quantity"]

def fetchitemlist(db, shopname):
    # To get the list of all item names.
    return list(fetchquantity(db, shopname).keys())

def fetchchanges(db, shopname):
    # To get the change log in list format.
    db.changedoc("shop")
    return db.data[shopname]["changes"]

def fetchmembers(db, shopname):
    # To get a dictionary with key as names and value as role.
    db.changedoc("shop")
    return db.data[shopname]["members"]

def additem(db, shopname, itemname, count = 1):
    # To addd a item into the shop of passed arg.
    db.changedoc("shop")

    if itemname in db.data[shopname]["quantity"].keys():
        db.data[shopname]["quantity"][itemname] += count
    else:
        db.data[shopname]["quantity"][itemname] = count

    timenow = time.ctime()
    db.data[shopname]["changes"].append([itemname, count, timenow])

    db.savedoc()

def removeitem(db, shopname, itemname, count = 1):
    # To remove a item from the shop of passed arg.
    db.changedoc("shop")

    if itemname in db.data[shopname]["quantity"].keys():
        db.data[shopname]["quantity"][itemname] -= count
    else:
        db.data[shopname]["quantity"][itemname] = 0

    timenow = time.ctime()
    db.data[shopname]["changes"].append([itemname, -count, timenow])

    db.savedoc()

def addmember(db, shopname, member, role):
    # To add a member to the shop. role options (owner / admin / cashier)
    db.changedoc("shop")

    if member in fetchmembers(db, shopname):
        return 0
    elif not role in ("owner", "admin", "cashier"):
        raise ValueError("Invalid role has been passed.")
    else:
        db.data[shopname]["members"][member] = role
        db.savedoc()
        return 1
    
def removemember(db, shopname, member):
    # To remove a member from the shop.
    db.changedoc("shop")

    if not member in fetchmembers(db, shopname):
        return 0
    else:
        del db.data[shopname]["members"][member]
        db.savedoc()
        return 1