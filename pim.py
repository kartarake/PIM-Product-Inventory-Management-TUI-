import math
import json
import mysql.connector as sql


#  _   _ _   _ _ _ _         
# | | | | |_(_) (_) |_ _   _ 
# | | | | __| | | | __| | | |
# | |_| | |_| | | | |_| |_| |
#  \___/ \__|_|_|_|\__|\__, |
#                      |___/ 
def fillspace(length, string):
    got = len(string)
    need = length
    fill = need - got

    del got, need
    return fill
    
def splitspace(length, string):
    got = len(string)
    fill = length - got

    half = fill / 2
    split1 = math.ceil(half)
    split2 = math.floor(half)

    return (split1, split2)
        

def boxify(string, width = None, align = "left"):
    linelist = string.split('\n')
    maxcharinline = len(max(linelist, key=len))

    if not(width == None):
        width = width
    else:
        width = maxcharinline + 4

    belt = list()
    
    topline = '.' + ('-' * (width - 2)) + '.'
    belt.append(topline)

    if align in ("left", "l"):
        for line in linelist:
            bwline = '| ' + line + (' ' * fillspace(width - 4, line)) + ' |'
            belt.append(bwline)

    elif align in ("right", "r"):
        for line in linelist:
            bwline = '| ' + (' ' * fillspace(width - 4, line)) + line + ' |'
            belt.append(bwline)

    elif align in ("centre", "center", "c"):
        for line in linelist:
            bwline = '| ' + (' ' * splitspace(width - 4, line)[0]) + line + (' ' * splitspace(width - 4, line)[1]) + ' |'
            belt.append(bwline)

    else:
        raise ValueError('Invalid align method is passed.')

    bottomline = "'" + ('-' * (width - 2)) + "'"
    belt.append(bottomline)

    final = '\n'.join(belt)
    return final

def simplify(string):
    return string.lower().strip()

def countmap(string):
    map = {}
    for char in string:
        if char in map:
            map[char] += 1
        else:
            map[char] = 1
    return map

def countmapsimilarity(string1, string2):
    map1 = countmap(string1)
    map2 = countmap(string2)

    similarity = 1
    for key in map1:
        if key in map2 and map1[key] == map2[key]:
            similarity *= 1.5
        elif key in map2:
            similarity *= 1.25
        else:
            pass

    return similarity

def smallstr(string1, string2):
    if len(string1) < len(string2):
        return string1
    else:
        return string2

def possimilarity(string1, string2):
    similar = 0
    for i in range(len(smallstr(string1, string2))):
        if string1[i] == string2[i]:
            similar += 1

    return similar/len(string1)*2

def similarity(string1, string2):
    constant = 1
    string1 = simplify(string1)
    string2 = simplify(string2)

    if string1[0] == string2[0]:
        constant *= 1.5
    if string1[-1] == string2[-1]:
        constant *= 1.5
    constant *= countmapsimilarity(string1, string2)
    constant *= possimilarity(string1, string2)
    return constant
    
def matchstr(iterable, string):
    consmap = {}
    for reference in iterable:
        wordsimilarity = similarity(string, reference)
        consmap[reference] = wordsimilarity
    
    currentmax = None
    consmap[currentmax] = -1
    for key in consmap:
        if currentmax is None or consmap[key] > consmap[currentmax]:
            currentmax = key

    return currentmax

def valuediff(ypos,i):
    if i>len(ypos)-2:
        return 0
    return ypos[i] - ypos[i+1]

def graphify(values):
    if values is None or len(values) == 0:
        raise ValueError("values must not be null or empty")

    xvalues = []
    yvalues = []
    for tuple in values:
        xvalues.append(tuple[0])
        yvalues.append(tuple[1])

    valuerange = max(xvalues) - min(xvalues)
    margin = valuerange / 10    
    upperlimit = max(yvalues) + margin
    lowerlimit = min(yvalues) - margin

    graphrange = upperlimit - lowerlimit
    if graphrange == 0:
        raise ValueError("graphrange must not be zero")

    graphunit = graphrange / 10
    graphmarked = []
    for i in range(1,11):
        graphmarked.append(graphunit*i)
    
    ypos = []
    for i in yvalues:
        for j in range(len(graphmarked)):
            if i < graphmarked[j]:
                ypos.append(len(graphmarked) - 1 - j)
                break
    
    graph = []
    for i in range(10):
        graph.append([])
    
    for i in range(len(ypos)):
        column = list(" " * 10)
        diff = valuediff(ypos,i)
        if diff == 0:
            column[ypos[i]] = "_"
        elif diff == 1:
            column[ypos[i]] = "/"
        elif diff == -1:
            column[ypos[i]] = "\\"
        elif diff > 1:
            for j in range(diff):
                column[ypos[i]-j] = "|"
                column[ypos[i]-j-1] = "/"
        elif diff < -1:
            for j in range(-diff):
                column[ypos[i]+j] = "|"
                column[ypos[i]+j+1] = "\\"
        else:
            pass

        for j in range(10):
            graph[j].append(column[j])

    for i in range(len(graph)):
        graph[i].insert(0, "| ")
        graph[i] = "".join(graph[i])
    
    graph.append("+"+"-"*(len(graph[i])-1))

    graph = "\n".join(graph)
    return graph

#  ____        _        _                    
# |  _ \  __ _| |_ __ _| |__   __ _ ___  ___ 
# | | | |/ _` | __/ _` | '_ \ / _` / __|/ _ \
# | |_| | (_| | || (_| | |_) | (_| \__ \  __/
# |____/ \__,_|\__\__,_|_.__/ \__,_|___/\___|
def init(dbname, host, user, password, shopname, multibranch):
    con = sql.connect(host=host, user=user, passwd=password)
    cursor = con.cursor()

    cursor.execute(f"create database if not exists {dbname};")
    cursor.execute(f"use {dbname}")

    cursor.execute("""create table if not exists shop (
                   shopname varchar(30) primary key,
                   multibranch int);""")
    
    record = (shopname, multibranch)
    cursor.execute(f"insert into shop values{record}")

    cursor.execute(f"""create table if not exists credentials (username varchar(30) primary key,
                   password varchar(64));""")
    
    cursor.execute(f"""create table if not exists {None}_itemdata (itemname varchar(30) primary key,
                   quantity int,
                   price float(10,4),
                   description text);""")
    
    cursor.execute(f"""create table if not exists {None}_changes (itemname varchar(30),
                   ccount int,
                   time datetime);""")
    
    cursor.execute(f"""create table if not exists {None}_members (
                   username varchar(30) primary key,
                   role varchar(30));""")
    
    con.commit()        
    return con

def mbinit(dbname, host, user, password, record):
    con = sql.connect(host=host, user=user, passwd=password)
    cursor = con.cursor()

    cursor.execute(f"create database if not exists {dbname};")
    cursor.execute(f"use {dbname}")

    cursor.execute("""create table if not exists shop (
                   shopname varchar(30) primary key,
                   multibranch int,
                   branchlist text,
                   trackers text);""")
    
    record = record + (json.dumps({}),)
    cursor.execute(f"insert into shop values{record};")

    cursor.execute(f"select branchlist from shop;")
    branchlist = json.loads(cursor.fetchone()[0])

    for branch in branchlist:
        cursor.execute(f"""create table if not exists credentials (username varchar(30) primary key,
                    password varchar(64));""")
            
        cursor.execute(f"""create table if not exists {branch}_itemdata (itemname varchar(30) primary key,
                    quantity int,
                    price float(10,4),
                    description text);""")
            
        cursor.execute(f"""create table if not exists {branch}_changes (itemname varchar(30),
                    ccount int,
                    time datetime);""")
            
        cursor.execute(f"""create table if not exists {branch}_members (
                    username varchar(30) primary key,
                    role varchar(30));""")
        
    return con
    
def connect(dbname, host, user, password):
    con = sql.connect(host=host, user=user, passwd=password, database=dbname)
    return con

def fetchtable(con, table):
    cursor = con.cursor()
    cursor.execute(f"select * from {table};")
    data = cursor.fetchall()
    return data

def puttable(con, table, grid):
    cursor = con.cursor()
    cursor.execute(f"delete from {table};")
    con.commit()
    
    for row in grid:
        insertrow(con, table, row)

    con.commit()

def insertrow(con, table, row):
    row = tuple(row)

    if None in row:
        row = insertwithnonestring(row)

    cursor = con.cursor()
    cursor.execute(f"insert into {table} values{row};")
    con.commit()

def insertwithnonestring(record):
    qstring = []
    qstring.append("(")
    for item in record:
        if type(item) == str:
            qstring.append("'")
            qstring.append(item)
            qstring.append("'")
            qstring.append(",")
        elif item == None:
            qstring.append("null")
            qstring.append(",")
        else:
            qstring.append(str(item))
            qstring.append(",")
    qstring.pop()
    qstring.append(")")
    qstring = "".join(qstring)
    return qstring

def deleterow(con, table, where):
    cursor = con.cursor()
    cursor.execute(f"delete from {table} where {where}")
    con.commit()

def disconnect(con):
    con.close()

def fetchtime(con):
    cursor = con.cursor()
    cursor.execute("select now();")
    time = str(cursor.fetchone()[0])
    return time

#  ____  _                     
# / ___|| |__   ___  _ __  ___ 
# \___ \| '_ \ / _ \| '_ \/ __|
#  ___) | | | | (_) | |_) \__ \
# |____/|_| |_|\___/| .__/|___/
#                   |_|        
def fetchitemdata(con, lwshop):
    # To get the itemdata holding dictionary.
    data = fetchtable(con, f"{lwshop}_itemdata")
    return data

def fetchitemrow(con, lwshop, itemname):
    # To get the row of the item in the shop.
    data = fetchitemdata(con, lwshop)

    for row in data:
        if row[0] == itemname:
            return row
    else:
        return None    

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
    data = fetchtable(con, f"{lwshop}_changes")
    return data

def fetchmembers(con, lwshop):
    # To get the data of members of that shop.
    data = fetchtable(con, f"{lwshop}_members")
    return data

def fetchrole(con, username, lwshop):
    # To fetch the role of the username
    data = fetchmembers(con, lwshop)
    
    for i in range(len(data)):
        if data[i][0] == username:
            break
    else:
        return None

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
    puttable(con, f"{lwshop}_members", data)

def newitem(con, itemname, price, desc, lwshop):
    # To insert a new item data
    record = (itemname, 0, price, desc)
    if not desc == None:
        insertrow(con, f"{lwshop}_itemdata", record)
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
    puttable(con, f"{lwshop}_itemdata", data)

    now = fetchtime(con)
    record = (itemname, count, now)
    insertrow(con, f"{lwshop}_changes", record)

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
    puttable(con, f"{lwshop}_itemdata", data)

    now = fetchtime(con)
    record = (itemname, -count, now)
    insertrow(con, f"{lwshop}_changes", record)

def addmember(con, member, role, lwshop):
    # To add a member to the shop. role options (owner / admin / clerk)
    record = (member, role)
    insertrow(con, f"{lwshop}_members", record)
    
def removemember(con, member, lwshop):
    # To remove a member from the shop.
    where = f"username = {member}"
    deleterow(con, f"{lwshop}_members", where)

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
    rdata = fetchtable(con, "shop")
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
    insertrow(con, "shop", record)

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

#     _                             _       
#    / \   ___ ___ ___  _   _ _ __ | |_ ___ 
#   / _ \ / __/ __/ _ \| | | | '_ \| __/ __|
#  / ___ \ (_| (_| (_) | |_| | | | | |_\__ \
# /_/   \_\___\___\___/ \__,_|_| |_|\__|___/
def getuserlist(con):
    # returns a list of all usernames.
    data = fetchtable(con, "credentials")
    usernamelist = []
    for row in data:
        usernamelist.append(row[0])
    return usernamelist
    
def new_account(con, username, password):
    # use this to create new account in db.
    try:
        usernamelist = getuserlist(con)

        if username in usernamelist:
            raise ValueError('Username already exists.')
        else:            
            record = (username, password)
            insertrow(con, "credentials", record)

        return 1
    
    except ValueError:
        return 0  


def addtoshop(con, username, role, lwshop):
    # adds the passed use to members table
    insertrow(con, f"{lwshop}_members", (username, role))

def doespassmatch(con, provided_username, provided_password):
    # checks if the provided username matches with stored one.
    data = fetchtable(con, "credentials")

    if not(provided_username in getuserlist(con)):
        raise ValueError("Username not in data")
    else:
        pass
    
    for row in data:
        if row[0] == provided_username:
            break  

    password = row[1]

    # returns true if password matches or returns false.
    return password == provided_password

#  __  __      _        _          
# |  \/  | ___| |_ _ __(_) ___ ___ 
# | |\/| |/ _ \ __| '__| |/ __/ __|
# | |  | |  __/ |_| |  | | (__\__ \
# |_|  |_|\___|\__|_|  |_|\___|___/

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
    itemlist = fetchitemlist(con, lwshop)

    data = fetchchanges(con, lwshop)
    mapping = {}
    for item in itemlist:
        mapping[item] = []
    for row in data:
        mapping[row[0]].append(row)
    end_time_map = {}
    for key in mapping:
        end_time_map[key] = days(str(mapping[key][-1][2]))
    timeperiod_map = {}
    for key in end_time_map:
        timeperiod_map[key] = end_time_map[key] - start_time

    return timeperiod_map


def issameyear(year, timestamp):
    if not type(timestamp) == str:
        timestamp = str(timestamp)
    return int(timestamp[0:4]) == year

def calc_inv_till(con, lwshop, index):
    changes = fetchchanges(con, lwshop)

    inventory = 0
    for i in range(index):
        item = changes[i][0]
        itemprice = fetchitemprice(con, item, lwshop)
        change = changes[i][1]
        inventory += change * itemprice
    return inventory

def first_appearance(con, lwshop, year):
    changes = fetchchanges(con, lwshop)

    for i in list(range(len(changes))):
        if issameyear(year, changes[i][2]):
            first_change_rowpos = i
            return first_change_rowpos
    else:
        return None
    
def last_appearance(con, lwshop, year):
    changes = fetchchanges(con, lwshop)

    for i in list(range(len(changes)))[::-1]:
        if issameyear(year, changes[i][2]):
            final_change_rowpos = i
            return final_change_rowpos
    else:
        return None

def costofgoods(con, lwshop, year):
    changes = fetchchanges(con, lwshop)

    first_change_rowpos = first_appearance(con, lwshop, year)
    final_change_rowpos = last_appearance(con, lwshop, year)

    if None in (first_change_rowpos, final_change_rowpos):
        return None

    total_cost = 0
    for i in range(first_change_rowpos, final_change_rowpos+1):
        change = changes[i][1]
        if change < 0:
            item = changes[i][0]
            itemprice = fetchitemprice(con, item, lwshop)
            total_cost += math.fabs(change) * itemprice

    return total_cost

def averageinv(con, lwshop, year):
    first_change_rowpos = first_appearance(con, lwshop, year)
    final_change_rowpos = last_appearance(con, lwshop, year)
    
    first_inventory = calc_inv_till(con, lwshop, first_change_rowpos+1)
    final_inventory = calc_inv_till(con, lwshop, final_change_rowpos+1)

    average_inventory = final_inventory - first_inventory / 2
    return average_inventory

def invturnover(con, lwshop, year):
    cost_of_goods_sold = costofgoods(con, lwshop, year)
    if cost_of_goods_sold == None:
        return None
    
    averageinventory = averageinv(con, lwshop, year)

    return cost_of_goods_sold / averageinventory


def invstockout(con, lwshop):
    # To calculate the stockout rate
    itemdata = fetchitemdata(con, lwshop)

    stockout = 0
    total = len(itemdata)
    if total == 0:
        return None

    for row in itemdata:
        if row[1] == 0:
            stockout += 1
    
    stockoutrate = stockout / total * 100
    return stockoutrate


def ABCanalysis(con, lwshop): 
    timestamp = input("Enter timestamp:")
    timeperiod_map = timeperiod(con,lwshop,timestamp)
    A=[]
    B=[]
    C=[]
    D=[]
    for i in timeperiod_map:
        stock = fetchitemquantity(con,i,lwshop)
        demand = timeperiod_map[i]
        if demand == 0:
            D.append(i)
        else:
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

    if len(D)!=0:
        print(D)
        print("(These items were only recently added and ABC analysis cannot be done)")
    else:
        pass


def timestamp_now(con):
    # Returns the current timestamp
    # Timestamp format: "YYYY-MM-DD HH:MM:SS"
    cursor = con.cursor()
    cursor.execute("select now();")
    timestamp = str(cursor.fetchall()[0][0])
    return str(timestamp)

def gettimediff(timestamp1, timestamp2):
    in_days1 = days(timestamp1)
    in_days2 = days(timestamp2)
    timediff = math.fabs(in_days1 - in_days2)
    return timediff

def first_time_of_item(con, item, lwshop):
    changes = fetchchanges(con, lwshop)

    for row in changes:
        if row[0] == item:
            return str(row[2])
    else:
        return None

def stockvelocity(con, lwshop):
    changes = fetchchanges(con, lwshop)
    itemlist = fetchitemlist(con, lwshop)

    qty_sold = {}
    velocity = {}
    for item in itemlist:
        qty_sold[item] = 0
        velocity[item] = 0

    for row in changes:
        change = row[1]
        if change < 0:
            item = row[0]
            qty_sold[item] += math.fabs(change)
   
    for item in qty_sold:
        now = timestamp_now(con)
        first_time = first_time_of_item(con, item, lwshop)
        timediff = gettimediff(now, first_time)
        if timediff:
            velocity[item] = qty_sold[item] / timediff
        else:
            velocity[item] = None

    return velocity

def fetchallyears(con,lwshop):
    changes = fetchchanges(con,lwshop)
    years = []
    for row in changes:
        if not int(str(row[2])[:4]) in years:
            years.append(int(str(row[2])[:4]))
    return years

#  __  __       _       
# |  \/  | __ _(_)_ __  
# | |\/| |/ _` | | '_ \ 
# | |  | | (_| | | | | |
# |_|  |_|\__,_|_|_| |_|

# Variable Dashboard
swidth = 153  
mysql_user = "root"
mysql_pass = "root"


def checksame(string1, string2):
    return string1.lower().strip() == string2.lower().strip()

def checkin(string, iterable):
    return string in [item.lower() for item in iterable]

def setup():
    str1 = r"""
    __        _______ _     ____ ___  __  __ _____   _____ ___    ____ ___ __  __ 
    \ \      / / ____| |   / ___/ _ \|  \/  | ____| |_   _/ _ \  |  _ \_ _|  \/  |
     \ \ /\ / /|  _| | |  | |  | | | | |\/| |  _|     | || | | | | |_) | || |\/| |
      \ V  V / | |___| |__| |__| |_| | |  | | |___    | || |_| | |  __/| || |  | |
       \_/\_/  |_____|_____\____\___/|_|  |_|_____|   |_| \___/  |_|  |___|_|  |_|
    """
    print(boxify(str1,width = swidth, align="centre"))
    str2 = "Setup"
    print(boxify(str2,width = swidth, align="centre"))
    print()

    print("--Step (1/3)--")
    username, password = fsignup()
    print()

    print("--Step (2/3)--")
    shopname = input("Enter your shop name : ")
    print()

    print("--Step (3/3)--")
    while True:
        string = "Do you want multi-branch system enabled?\n\t[1] Yes\n\t[2] No\n> "
        choice = input(string)
        if choice in ("1","2"):
            break
        else:
            print(boxify("Invalid Choice", width=swidth))
    print()

    if choice == "1":
        choice = 1
        branchlist = json.dumps(askbranchlist())
        return (username, password, shopname, choice, branchlist)
    
    else:
        choice = 0
        return (username, password, shopname, choice)        
    
def askbranchlist():
    branchlist = []
    while True:
        branch = input("Enter branch name ('end' to terminate loop): ")
        if branch in branchlist:
            print(boxify("Branch already exists!", width=swidth))
            continue
        elif checkin(branch,("","end","stop","break","done")):
            break
        else:
            branchlist.append(branch)
    return branchlist

def landerpage(): # The first page upon opening the application.
    str1 = r"""
    __        _______ _     ____ ___  __  __ _____   _____ ___    ____ ___ __  __ 
    \ \      / / ____| |   / ___/ _ \|  \/  | ____| |_   _/ _ \  |  _ \_ _|  \/  |
     \ \ /\ / /|  _| | |  | |  | | | | |\/| |  _|     | || | | | | |_) | || |\/| |
      \ V  V / | |___| |__| |__| |_| | |  | | |___    | || |_| | |  __/| || |  | |
       \_/\_/  |_____|_____\____\___/|_|  |_|_____|   |_| \___/  |_|  |___|_|  |_|
    """
    print(boxify(str1,width = swidth, align="centre"))
    str2 = "[1] Login      |      [2] Sign up"
    print(boxify(str2,width = swidth, align="centre"))

    while True:
        choice = input('Enter respective number to continue : ')

        if choice in ('1', '2','login','signup'):
            break
        else:
            print(boxify('Invalid choice', width = swidth, align = "centre"))

    if choice in ('1', 'login'):
        return 'login'
    else:
        return 'signup'
    
def signup(con): # The page where they can sign up an account.
    print(boxify("Sign Up", width = swidth))
    while True:
        username = input("Enter username: ")
        l1 = getuserlist(con)
        if username in l1:
            print(boxify("Username already taken", width = swidth))
        else:
            break 
    
    while True:
        password = input("Enter password: ")
        if len(password) < 5:
            print(boxify("The given password has less than 5 characters", width = swidth))
        else:
            break
    
    while True:
        password1 = input("Confirm password: ")
        if password1 == password:
            break
        else:
            print(boxify("The password does not match"))
    
    new_account(con,username,password)
    return username

def fsignup():
    print(boxify("Sign Up", width = swidth))
    username = input("Enter username: ")
    
    while True:
        password = input("Enter password: ")
        if len(password) < 5:
            print(boxify("The given password has less than 5 characters", width = swidth))
        else:
            break
    
    while True:
        password1 = input("Confirm password: ")
        if password1 == password:
            break
        else:
            print(boxify("The password does not match"))

    return (username,password)


def login(con):
    print(boxify("Login", width = swidth))
    while True:
        username = input("Enter username : ")
        l1 = getuserlist(con)
        if username in l1:
            break
        else:
            print(boxify("The given username does not exist", width = swidth))
    while True:
        password = input("Enter password : ")
        valuepassword = doespassmatch(con,username,password)
        if valuepassword == True:
            break
        else:
            print(boxify("The given password is incorrect", width = swidth))
    return username

def shopmenu():
    str1 = "[1] Add Stock    |    [2] Remove Stock     |    [3] Inventory   |    [4] Insights     |   [5] Manage shop   |   [6] Exit"
    print(boxify(str1,width = swidth,align = "centre"))
    while True:
        choice = input('Enter respective choice to continue : ')
        if choice in ('1', '2','3','4','5','6','Add Stock','Insights','Manage shop','Remove Stock','Inventory','Back'):
            break
        else:
            print(boxify('Invalid choice', width = swidth, align = "centre"))
    
    if choice == "Add Stock":
        choice = '1'
    elif choice == 'Remove Stock':
        choice = '2'
    elif choice == 'Insights':
        choice = '4'
    elif choice == 'Manage shop':
        choice = '5'
    elif choice == 'Back':
        choice = '6'
    else:
        pass

    return choice

def memshopmenu():
    str1 = "[1] Add Stock    |    [2] Remove Stock     |    [3] Inventory   |    [4] Insight     |     [5] Switch Branch     |    [6] Exit"
    print(boxify(str1,width = swidth,align = "centre"))
    while True:
        choice = input('Enter respective choice to continue : ')
        if choice in ('1', '2','3','4','5','Add Stock','Insights','Remove Stock','Inventory','Back'):
            break
        else:
            print(boxify('Invalid choice', width = swidth, align = "centre"))
    
    if choice == "Add Stock":
        choice = '1'
    elif choice == 'Remove Stock':
        choice = '2'
    elif choice == 'Insights':
        choice = '4'
    elif choice == 'Switch Branch':
        choice = '5'
    elif choice == 'Exit':
        choice = '6'
    else:
        pass

    return choice

def ask_itemname():
    while True:
        itemname = input("Enter item name : ")
        if len(itemname)>30:
            print("The given item name exceeds the character limit of 30")
        elif len(itemname)==0:
            print("The givem item name is empty")
        else:
            break
    return itemname

def ask_quantity():
    while True:
        quantity = input("Enter quantity (units) : ")
        if quantity.isdigit():
            quantity = int(quantity)
            break
        else:
            print("The given string is not an integer")
    return quantity

def ask_price():
    while True:
        price = input("Enter price per unit : ")
        price = price.replace(',','')

        if not price.isdigit():
            print(boxify('Please enter number', width=swidth))
        else:
            price = float(price)
            break
    return price

def ask_desc():
    print('Enter product description (optional). Just press enter to skip/end')
    para = []
    while True:
        line = input(">")
        if line == '':
            break
        else:
            para.append(line)
    if para == "":
        return None
    else:
        return str("\n".join(para))

def addingitem(con, lwshop):
    print()
    print(boxify("Adding Items", width=swidth))

    itemname = ask_itemname()
    quantity = ask_quantity()

    if not itemname in fetchitemlist(con, lwshop): # introducing new item to table.
        price = ask_price()
        desc = ask_desc()
        newitem(con, itemname, price, desc, lwshop)
    
    additem(con, itemname, lwshop, quantity)
    print(boxify("Sucessfully added item", width = swidth))


def toremoveitem(con, lwshop):
    print()
    print(boxify("Removing an item", width = swidth))
    while True:
        itemname = input("Enter itemname: ")
        itemlist = fetchitemlist(con, lwshop)
        if itemname not in itemlist:
            print("The given item is not in the shop")
        else:
            break
    
    while True:
        quantity = int(input("Enter the no. of items to remove: "))
        actualquantity = fetchitemquantity(con, itemname, lwshop)
        if quantity > actualquantity:
            print("The given amount is greater than the amount of items in the shop")
        else:
            break    

    removeitem(con, itemname, lwshop, count = quantity)
    print(boxify("Sucessfully removed.", width = swidth))

def manageshopmenu():
    print("\n")
    str1 = "[1] Change Working Branch    |    [2] Permissions    |    [3] Export log    |   [4] Back"
    print(boxify(str1,width = swidth,align = "centre"))
    while True:
        choice = input('Enter respective choice to continue : ')
        if choice.lower() in ('1', '2','3','4','change working branch','permissions','export log','back'):
            if choice.lower() == "change working branch":
                choice = '1'
            elif choice.lower() == 'permissions':
                choice = '2'
            elif choice.lower() == 'export log':
                choice = '3'
            elif choice.lower() == 'back':
                choice = '4'
            break
        else:
            print(boxify('Invalid choice', width = swidth, align = "centre"))
    return choice

def askbranch(con):
    print(boxify("Select Branch",width=swidth))
    while True:
        branch = input("Enter branch : ")
        if branch in fetchbranchlist(con):
            break
        else:
            print(boxify("Invalid branch name", width=swidth))
    print()
    return branch

def exportlog(con, lwshop):
    f = open("log.txt","w")
    log = fetchchanges(con, lwshop)
    for i in log:
        f.write(f"[{i[2]}] Count of item {i[0]} changed by {i[1]}\n") 
    f.close()
    print(boxify("Wrote log to log.txt", width=swidth))
    print()

def changeworkingbranch(con, person, lwshop):
    branch = askbranch(con)
    lwshop = branch
    setlwshop(con, person, lwshop)
    print(boxify("Sucessfully changed working branch", width=swidth))
    print()
    
    role = fetchrole(con, person, lwshop)
    if role == "owner":
        owner_loop(con, recordbackup.copy(), lwshop)
    elif role == "admin":
        admin_loop(con, recordbackup.copy(), lwshop)
    elif role == "member":
        member_loop(con, recordbackup.copy(), lwshop)
    else:
        string = "You are not registered in this branch. Ask branch admin to whitelist you"
        print(boxify(string, width = swidth))

def addmember(con,member,role,lwshop):
    record = ( member, role)
    insertrow(con,lwshop+"_members",record)

def removemember(con,member,lwshop):
    deleterow(con,lwshop+"_members","username ='"+member+"'")

def Addmember(con, lwshop):
    while True:
        member = input("Enter member name: ")
        role = input("Enter role: ").lower().strip()
        if checkmemberexists(con, member, lwshop):
            print("The given member is already in the shop")
        elif role not in ("owner", "admin", "member"):
            print("Invalid role")
        else:
            break
    addmember(con, member, role, lwshop)

def adminAddmember(con, lwshop):
    while True:
        member = input("Enter member name: ")
        role = input("Enter role: ").lower().strip()
        if checkmemberexists(con, member, lwshop):
            print("The given member is already in the shop")
        elif role not in ("member", "admin"):
            print("Invalid role")
        else:
            break
    addmember(con, member, role, lwshop)

def Removemember(con, lwshop):
    while True:        
        member = input("Enter member name: ")
        if checkmemberexists(con, member, lwshop):
            break
        else:
            print("The given member is not in the shop")
    removemember(con, member, lwshop)

def adminRemovemember(con, lwshop):
    while True:        
        member = input("Enter member name: ")
        if checkmemberexists(con, member, lwshop):
            break
        role = fetchrole(con, member, lwshop)
        if role in ("owner",):
            print("Permission denied")
        else:
            print("The given member is not in the shop")
    removemember(con, member, lwshop)

def Changepermission(con, lwshop):
    memberlist = fetchmembers(con, lwshop)

    while True:
        member = input("Enter username : ").lower()
        if not checkmemberexists(con, member, lwshop):
            print("There is no such username in our database.")
        else:
            break

    while True:
        role = input("Enter new role : ").lower()
        if not checkin(role, ("owner","admin","member")):
            print("Invalid role has been assigned. Try again.")
        else:
            break

    pos = fetchmemberpos(con, member, lwshop)
    memberlist[pos] = (member, role)
    puttable(con, f"{lwshop}_members", memberlist)

    print(boxify("Sucessfully updated role of "+member, width = swidth))

def adminChangepermission(con, lwshop):
    memberlist = fetchmembers(con, lwshop)

    while True:
        member = input("Enter username : ").lower()
        if not checkmemberexists(con, member, lwshop):
            print("There is no such username in our database.")
        elif fetchrole(con, member, lwshop) in ("owner",):
            print("Permission denied")
        else:
            break

    while True:
        role = input("Enter new role : ").lower()
        if not checkin(role, ("admin","member")):
            print("Invalid role has been assigned. Try again.")
        else:
            break

    pos = fetchmemberpos(con, member, lwshop)
    memberlist[pos] = (member, role)
    puttable(con, f"{lwshop}_members", memberlist)

    print(boxify("Sucessfully updated role of "+member, width = swidth)) 

def ownermenu(con, lwshop):
    while True:
        print("\n")
        str1 = "[1] Add member    |    [2] Remove member    |    [3] Change permission    |    [4] Back"
        print(boxify(str1,width = swidth,align = "centre"))
        while True:
            choice = input('Enter respective choice to continue : ')
            if choice in ('1', '2','3','4'):
                break
            else:
                print(boxify('Invalid choice', width = swidth, align = "centre"))
        if choice == "1":
            Addmember(con, lwshop)
        elif choice == "2":
            Removemember(con, lwshop)
        elif choice == "3":
            Changepermission(con, lwshop)
        elif choice == "4":
            break

def adminmenu(con, lwshop):
    while True:
        print("\n")
        str1 = "[1] Add member    |    [2] Remove member    |    [3] Change permission    |    [4] Back"
        print(boxify(str1,width = swidth,align = "centre"))
        while True:
            choice = input('Enter respective choice to continue : ')
            if choice in ('1', '2','3','4'):
                break
            else:
                print(boxify('Invalid choice', width = swidth, align = "centre"))
        if choice == "1":
            adminAddmember(con, lwshop)
        elif choice == "2":
            adminRemovemember(con, lwshop)
        elif choice == "3":
            adminChangepermission(con, lwshop)
        elif choice == "4":
            break

def inventoryturnover_tui(con, lwshop):
    print("\n")
    print(boxify("Inventory Turnover Rate", width = swidth))

    plots = []
    years = fetchallyears(con, lwshop)
    for year in years:
        plots.append([year, invturnover(con,lwshop,year)])

    if len(plots) <= 2:
        print(boxify("Add more records for graph", width=swidth))
    else:
        string = graphify(plots)
        print(boxify(string, width = swidth))
    
    for set in plots:
        print(f"{set[0]}:{set[1]}")

def stockout_tui(con, lwshop):
    stockout = invstockout(con, lwshop)
    print(boxify("Stockout Rate", width = swidth))
    string = f"\nEver since shop started, stockout rate is {stockout}\n"
    print(boxify(string, width = swidth))

def ABCanalysis_tui(con, lwshop):
    print(boxify("ABC Analysis", width = swidth))
    ABCanalysis(con, lwshop)

def stockvelocity_tui(con, lwshop):
    print(boxify("Stock Velocity", width = swidth))
    velocity = stockvelocity(con, lwshop)
    for key in velocity:
        if velocity[key] == None:
            print(key, ":", "No value yet")
        else:
            print(key, ":", velocity[key], "units/day")

def insightmenu(con, lwshop):
    print("\n")
    menu = """\t[1] Inventory Turnover Rate
\t[2] Stockout Rate
\t[3] ABC Analysis
\t[4] Stock Velocity
\t[5] Back"""
    while True:
        print(boxify("Insights available", width = swidth))
        print(menu)
        choice = input("Enter respective number : ")
        if not choice in ("1", "2", "3", "4", "5"):
            print("Invalid choice")
        else:
            break

    if choice == '1':
        inventoryturnover_tui(con, lwshop)
        return 1

    elif choice == '2':
        stockout_tui(con, lwshop)
        return 1

    elif choice == '3':
        ABCanalysis_tui(con, lwshop)
        return 1

    elif choice == '4':
        stockvelocity_tui(con, lwshop)
        return 1

    elif choice == '5':
        return 0

    else:
        print("Invalid choice")

def insight_loop(con, lwshop):
    while True:
        signal = insightmenu(con, lwshop)
        if signal == 0:
            break
        else:
            pass

def display_iteminfo(con, lwshop, itemname):
    print()
    item = fetchitemrow(con, lwshop, itemname)
    print(boxify(item[0], width = swidth))
    print("Qty :",item[1],"units")
    print("Price : ₹",item[2])
    print("Description :")
    if item[3] in (None, ""):
        print("No description available")
    else:
        print(item[3])
    input()

def search_item(con, lwshop):
    itemname = input("Enter item name : ")
    itemlist = fetchitemlist(con, lwshop)
    if itemname in itemlist:
        display_iteminfo(con, lwshop, itemname)
    else:
        possibility = matchstr(itemlist, itemname)
        print(f"We could not find \"{itemname}\". Did you mean \"{possibility}\"?")
        choice = input("Enter [y/n] : ").lower().strip()
        if choice == "y":
            display_iteminfo(con, lwshop, possibility)
        elif choice == "n":
            print("try again..")
        else:
            print("Invalid choice")

def display_inventory(con, lwshop):
    print()
    print()
    if lwshop:
        print(boxify("Inventory - " + lwshop.title(), width = swidth))
    else:
        print(boxify("Inventory", width = swidth))

    page = 0
    itemlist = fetchitemlist(con, lwshop)
    total_pages = len(itemlist) // 10 + 1

    while True:
        print()
        pagelist = itemlist[page*10:page*10+10]
        if pagelist == []:
            print("No items were found in your inventory.")
            break
        
        print(boxify(f"Page : {page+1} / {total_pages}", width = swidth))
        for i in range(len(pagelist)):
            print(f"[{i+1}] {pagelist[i]}")
        string = f" [{i+2}] Previous Page |  [{i+3}] Next Page  |   [{i+4}] Search  |  [{i+5}] Back"
        print(boxify(string, width=swidth, align="centre"))

        expected = []
        for j in range(1,i+6):
            expected.append(str(j))

        while True:
            choice = input("Enter respective number to continue : ")
            if choice in expected:
                break
            else:
                print("Invalid choice")

        if choice == str(i+2):
            if page > 0:
                page -= 1
            else:
                print("Already on first page")
                input("[press enter to continue]")

        elif choice == str(i+3):
            if page < total_pages-1:
                page += 1
            else:
                print("Already on last page")
                input("[press enter to continue]")
        
        elif choice == str(i+4):
            search_item(con, lwshop)

        elif choice == str(i+5):
            break

        else:
            itemname = pagelist[int(choice)-1]
            display_iteminfo(con, lwshop, itemname)


def main_connect():
    # connecting to the mysql database

    try: # Not first time
        con = connect(
            "pim",
            "localhost",
            mysql_user,
            mysql_pass,
        )
        followup = landerpage()

        if followup == "signup": # to signup page
            person = signup(con)
        elif followup == "login": # to login page
            person = login(con)
        else:
            print(boxify("Neglience of signing up", width=swidth))
        del followup

        data = fetchshops(con)
        record = [person]
        if data[1]:
            record.extend([data[0], data[1], data[2], data[3]])
        else:
            record.extend([data[0], data[1]])

    except Exception: # first time
        record = setup()

        username = record[0]
        password = record[1]
        
        record = (record[0],) + record[2:] + ("{}",)

        if not record[2]:
            con = init(
                "pim",
                "localhost",
                mysql_user,
                mysql_pass,
                shopname = record[1],
                multibranch = record[2]
            )
        else:
            con = mbinit(
                "pim",
                "localhost",
                mysql_user,
                mysql_pass,
                record[1:-1]
            )
        
        person = record[0]
        new_account(con, username, password)

        if len(record) == 5:
            branchlist = json.loads(record[3])
            for branch in branchlist:
                addtoshop(con, username, "owner", branch)

        else:
            addtoshop(con, username, "owner", "None")

    return con, record

def manageshoploop(con, lwshop, person):
    while True:
        followup1 = manageshopmenu()
        if followup1 == "1":
            changeworkingbranch(con, person, lwshop)
        elif followup1 == "2":
            ownermenu(con, lwshop)
        elif followup1 == "3":
            exportlog(con, lwshop)
        elif followup1 == "4":
            break
        else:
            print("Invalid Input!!")

def adminmanageshoploop(con, lwshop, person):
    while True:
        followup1 = manageshopmenu()
        if followup1 == "1":
            changeworkingbranch(con, person, lwshop)
        elif followup1 == "2":
            adminmenu(con, lwshop)
        elif followup1 == "3":
            exportlog(con, lwshop)
        elif followup1 == "4":
            break
        else:
            print("Invalid Input!!")

def convifnot(record):
    if type(record[4]) == str:
        record[4] = json.loads(record[4])
    return record[4]

def owner_loop(con, record, lwshop):
    # main loop for owner
    person = record[0]

    while True:
        print("\n")
        if not record[2]:
            print(boxify(record[1].title(), width=swidth, align="centre"))

        elif person in convifnot(record):
            print(boxify(record[1].title() + "-" + lwshop.title(), width=swidth, align="centre"))

        else:
            lwshop = askbranch(con)
            setlwshop(con, person, lwshop)

            data = fetchshops(con)
            record = [person]+[data[0], data[1], json.loads(data[2]), json.loads(data[3])]
            print(boxify(record[1].title() + "-" + lwshop.title(), width=swidth, align="centre"))

        followup = shopmenu()

        if followup == '1': # Adding an item
            addingitem(con, lwshop)

        elif followup == "2": # Removing an item
            toremoveitem(con, lwshop)

        elif followup == "5": # Manage shop option
            manageshoploop(con, lwshop, person)

        elif followup == '4': # Insights
            insight_loop(con, lwshop)

        elif followup == "3": # Inventory
            display_inventory(con, lwshop)

        elif followup == "6": # Exit
            break

        else:
            print(boxify("Invalid choice", width = swidth))

def admin_loop(con, record, lwshop):
    # main loop for owner
    person = record[0]

    while True:
        print("\n")
        if not record[2]:
            print(boxify(record[1].title(), width=swidth, align="centre"))

        elif person in record[4]:
            print(boxify(record[1].title() + "-" + lwshop.title(), width=swidth, align="centre"))

        else:
            lwshop = askbranch(con)
            setlwshop(con, person, lwshop)

            data = fetchshops(con)
            record = [person]+[data[0], data[1], json.loads(data[2]), json.loads(data[3])]
            print(boxify(record[1].title() + "-" + lwshop.title(), width=swidth, align="centre"))

        followup = shopmenu()

        if followup == '1': # Adding an item
            addingitem(con, lwshop)

        elif followup == "2": # Removing an item
            toremoveitem(con, lwshop)

        elif followup == "5": # Manage shop option
            adminmanageshoploop(con, lwshop, person)

        elif followup == '4': # Insights
            insight_loop(con, lwshop)

        elif followup == "3": # Inventory
            display_inventory(con, lwshop)

        elif followup == "6": # Exit
            break

        else:
            print(boxify("Invalid choice", width = swidth))

def member_loop(con, record, lwshop):
    # main loop for owner
    person = record[0]

    while True:
        print("\n")
        if not record[2]:
            print(boxify(record[1].title(), width=swidth, align="centre"))

        elif person in record[4]:
            print(boxify(record[1].title() + "-" + lwshop.title(), width=swidth, align="centre"))

        else:
            lwshop = askbranch(con)
            setlwshop(con, person, lwshop)

            data = fetchshops(con)
            record = [person]+[data[0], data[1], json.loads(data[2]), json.loads(data[3])]
            print(boxify(record[1].title() + "-" + lwshop.title(), width=swidth, align="centre"))

        followup = memshopmenu()

        if followup == '1': # Adding an item
            addingitem(con, lwshop)

        elif followup == "2": # Removing an item
            toremoveitem(con, lwshop)

        elif followup == "5": # Switch Branch
            changeworkingbranch(con, person, lwshop)

        elif followup == "6": # Exit
            break

        elif followup == '4': # Insights
            insight_loop(con, lwshop)

        elif followup == "3": # Inventory
            display_inventory(con, lwshop)

        else:
            print(boxify("Invalid choice", width = swidth))

def main():
    # Connecting & logging into account
    global recordbackup

    con, record = main_connect()
    print(boxify("Sucessfully connected to the application!", width=swidth))
    print("\n")

    # Main loop
    if not record[2]:
        lwshop=None

    elif record[0] in eval(record[4]):
        lwshop = eval(record[4])[record[0]]

    else:
        lwshop = askbranch(con)
        record = list(record)
        record[4] = eval(record[4])
        record[4][record[0]] = lwshop
        setlwshop(con, record[0], lwshop)

    try:
        role = fetchrole(con, record[0], lwshop)
    except Exception:
        role = None

    recordbackup = record.copy()
        
    if role == "owner":
        owner_loop(con, record, lwshop)
    elif role == "admin":
        admin_loop(con, record, lwshop)
    elif role == "member":
        member_loop(con, record, lwshop)
    elif role == None:
        string = "You are not registered in this branch. Ask branch admin to whitelist you"
        print(boxify(string, width = swidth))

    # Disconnecting from mysql
    disconnect(con)


if __name__ == "__main__":
    main()
