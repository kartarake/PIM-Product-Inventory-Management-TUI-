from modules.boxify import boxify

import modules.accounts
import modules.database
import modules.metrics
import modules.shops

import json

# Variable Dashboard
swidth = 170    
mysql_user = "root"
mysql_pass = "mysql"


#testing commit
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
        l1 = modules.accounts.getuserlist(con)
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
    
    modules.accounts.new_account(con,username,password)

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
        l1 = modules.accounts.getuserlist(con)
        if username in l1:
            break
        else:
            print(boxify("The given username does not exist", width = swidth))
    while True:
        password = input("Enter password : ")
        valuepassword = modules.accounts.doespassmatch(con,username,password)
        if valuepassword == True:
            break
        else:
            print(boxify("The given password is incorrect", width = swidth))
    return username

def shopmenu():
    str1 = "[1] Add Stock    |    [2] Remove Stock     |    [3] Inventory   |    [4] Insights     |   [5] Manage shop   |   [6] Back"
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

    if not itemname in modules.shops.fetchitemlist(con, lwshop): # introducing new item to table.
        price = ask_price()
        desc = ask_desc()
        modules.shops.newitem(con, itemname, price, desc, lwshop)
    
    modules.shops.additem(con, itemname, lwshop, quantity)
    print(boxify("Sucessfully added item", width = swidth))


def toremoveitem(con, lwshop):
    print()
    print(boxify("Removing an item", width = swidth))
    while True:
        itemname = input("Enter itemname: ")
        itemlist = modules.shops.fetchitemlist(con, lwshop)
        if itemname not in itemlist:
            print("The given item is not in the shop")
        else:
            break
    
    while True:
        quantity = int(input("Enter the no. of items to remove: "))
        actualquantity = modules.shops.fetchitemquantity(con, itemname, lwshop)
        if quantity > actualquantity:
            print("The given amount is greater than the amount of items in the shop")
        else:
            break    

    modules.shops.removeitem(con, itemname, lwshop, count = quantity)
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
        if branch in modules.shops.fetchbranchlist(con):
            break
        else:
            print(boxify("Invalid branch name", width=swidth))
    print()
    return branch

def exportlog(con):
    f = open("log.txt","w")
    log = modules.shops.fetchchanges(con)
    for i in log:
        f.write(f"[{i[2]}] Count of item {i[0]} changed by {i[1]}") 
    f.close()
    print(boxify("Wrote log to log.txt", width=swidth))
    print()

def addmember(con,member,role,lwshop):
    record = ( member, role)
    modules.database.insertrow(con,lwshop+"_members",record)

def removemember(con,member,lwshop):
    modules.database.deleterow(con,lwshop+"_members","username ='"+member+"'")

def Addmember(con, lwshop):
    while True:
        member = input("Enter member name: ")
        role = input("Enter role: ")
        if modules.shops.checkmemberexists(con, member, lwshop):
            print("The given member is already in the shop")
        else:
            break
    addmember(con, member, role, lwshop)

def Removemember(con, lwshop):
    while True:        
        member = input("Enter member name: ")
        if modules.shops.checkmemberexists(con, member, lwshop):
            break
        else:
            print("The given member is not in the shop")
    removemember(con, member, lwshop)

def Changepermission(con, lwshop):
    memberlist = modules.shops.fetchmembers(con, lwshop)

    while True:
        member = input("Enter username : ").lower()
        if not modules.shops.checkmemberexists(con, member, lwshop):
            print("There is no such username in our database.")
        else:
            break

    while True:
        role = input("Enter new role : ").lower()
        if not checkin(role, ("owner","admin","member")):
            print("Invalid role has been assigned. Try again.")
        else:
            break

    pos = modules.shops.fetchmemberpos(con, member, lwshop)
    memberlist[pos] = (member, role)
    modules.database.puttable(con, f"{lwshop}_members", memberlist)

    print(boxify("Sucessfully updated role of "+member, width = swidth)) 

def ownermenu(con, lwshop):
    while True:
        print("\n")
        str1 = "[1] Add member    |    [2] Remove member    |    [3] Change permission    |    [4] Back"
        print(boxify(str1,width = swidth,align = "centre"))
        while True:
            choice = input('Enter respective choice to continue : ')
            if choice in ('1', '2','3','4','Add member','Change permission','Remove member','Back'):
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

def inventoryturnover_tui(con, lwshop):
    invturnover = modules.metrics.invturnover(con, lwshop)
    print(boxify("Inventory Turnover Rate", width = swidth))
    string = f"\nEver since shop started, inventory turnover rate is {invturnover}\n"
    print(boxify(string, width = swidth))

def stockout_tui(con, lwshop):
    stockout = modules.metrics.invstockout(con, lwshop)
    print(boxify("Stockout Rate", width = swidth))
    string = f"\nEver since shop started, stockout rate is {stockout}\n"
    print(boxify(string, width = swidth))

def ABCanalysis_tui(con, lwshop):
    print(boxify("ABC Analysis", width = swidth))
    modules.metrics.ABCanalysis(con, lwshop)

def insightmenu(con, lwshop):
    menu = """\t[1] Inventory Turnover Rate
\t[2] Stockout Rate
\t[3] ABC Analysis
\t[4] Back"""
    while True:
        print(boxify("Insights available", width = swidth))
        print(menu)
        choice = input("Enter respective number : ")
        if not choice in ("1", "2", "3", "4"):
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

def main_connect():
    # connecting to the mysql database

    try: # Not first time
        con = modules.database.connect(
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

        data = modules.shops.fetchshops(con)
        record = [person]
        if data[1]:
            record.extend([data[0], data[1], json.loads(data[2]), json.loads(data[3])])
        else:
            record.extend([data[0], data[1]])

    except Exception: # first time
        record = setup()

        username = record[0]
        password = record[1]
        
        record = (record[0],) + record[2:] + ("{}",)

        if not record[2]:
            con = modules.database.init(
                "pim",
                "localhost",
                mysql_user,
                mysql_pass,
                shopname = record[1],
                multibranch = record[2]
            )
        else:
            con = modules.database.mbinit(
                "pim",
                "localhost",
                mysql_user,
                mysql_pass,
                record[1:-1]
            )
        
        person = record[0]
        modules.accounts.new_account(con, username, password)

        if len(record) == 5:
            branchlist = json.loads(record[3])
            for branch in branchlist:
                modules.accounts.addtoshop(con, username, "owner", branch)

        else:
            modules.accounts.addtoshop(con, username, "owner", "None")

    return con, record

def owner_loop(con, record, lwshop):
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
            modules.shops.setlwshop(con, person, lwshop)

            data = modules.shops.fetchshops(con)
            record = [person]+[data[0], data[1], json.loads(data[2]), json.loads(data[3])]
            print(boxify(record[1].title() + "-" + lwshop.title(), width=swidth, align="centre"))

        followup = shopmenu()

        if followup == '1': # Adding an item
            addingitem(con, lwshop)

        elif followup == "2": # Removing an item
            toremoveitem(con, lwshop)

        elif followup == "5": # Manage shop option
            ownermenu(con, lwshop)

        elif followup == '4': # Insights
            insight_loop(con, lwshop)

        elif followup == "3": # Inventory
            pass

        elif followup == "6":
            break

        else:
            print(boxify("Invalid choice", width = swidth))

def main():
    # Connecting & logging into account
    con, record = main_connect()

    # Main loop
    if not record[2]:
        lwshop=None

    elif record[0] in record[4]:
        lwshop = record[4][record[0]]

    else:
        lwshop = askbranch(con)
        record = list(record)
        record[4] = eval(record[4])
        record[4][record[0]] = lwshop
        modules.shops.setlwshop(con, record[0], lwshop)

    try:
        role = modules.shops.fetchrole(con, record[0], lwshop)
    except Exception:
        role = None
        
    if role == "owner":
        owner_loop(con, record, lwshop)
    elif role == None:
        string = "You are not registered in any branch. Please wait"
        print(boxify(string, width = swidth))

    # Disconnecting from mysql
    modules.database.disconnect(con)


if __name__ == "__main__":
    main()