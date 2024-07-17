from modules.boxify import boxify

import modules.accounts
import modules.database
import modules.shops

import credentials
import json

# Variable Dashboard
swidth = 170



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
        string = "Do you want multi-branch system enabled?\n\t[1] Yes\n\t[2] No\n>"
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
    print()
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
        username = input("Enter username:")
        l1 = modules.accounts.getuserlist(con)
        if username in l1:
            print(boxify("Username already taken", width = swidth))
        else:
            break 
    
    while True:
        password = input("Enter password:")
        if len(password) < 5:
            print(boxify("The given password has less than 5 characters", width = swidth))
        else:
            break
    
    while True:
        password1 = input("Confirm password:")
        if password1 == password:
            break
        else:
            print(boxify("The password does not match"))
    
    modules.accounts.new_account(con,username,password)

def fsignup():
    print(boxify("Sign Up", width = swidth))
    username = input("Enter username:")
    
    while True:
        password = input("Enter password:")
        if len(password) < 5:
            print(boxify("The given password has less than 5 characters", width = swidth))
        else:
            break
    
    while True:
        password1 = input("Confirm password:")
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

def addingitem(con):
    while True:
        itemname = input("Enter item name : ")
        if len(itemname)>64:
            print("The given item name exceeds the character limit of 64")
        elif len(itemname)==0:
            print("The givem item name is empty")
        else:
            break

    while True:
        quantity = input("Enter quantity (units) : ")
        if quantity.isdigit():
            quantity = int(quantity)
            break
        else:
            print("The given string is not an integer")

    while True:
        price = input("Enter price per unit : ")
        price = price.replace(',','')

        if not price.isdigit():
            print(boxify('Please enter number', width=swidth))
        else:
            price = float(price)
            break

    print('Enter product description (optional). Just press enter to skip/end')
    para = []
    while True:
        line = input(">")
        if line == '':
            break
        else:
            para.append(line)
    desc = str('\n'.join(para))
    print(type(desc))
    if desc == '':
        desc = None

    modules.shops.newitem(con, itemname, price, desc)
    modules.shops.additem(con, itemname, quantity)

def toremoveitem(con):
    while True:
        itemname = input("Enter itemname:")
        itemlist = modules.shops.fetchitemlist(con)
        if itemname not in itemlist:
            print("The given item is not in the shop")
        else:
            break
    
    while True:
        quantity = int(input("Enter the no. of items to remove:"))
        actualquantity = modules.shops.fetchitemquantity(con, itemname)
        if quantity > actualquantity:
            print("The given amount is greater than the amount of items in the shop")
        else:
            break    

    modules.shops.removeitem(con, itemname, count = quantity)

def manageshopmenu():
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

def main():
    # app

    # connecting to the mysql database
    try: # Not first time
        con = modules.database.connect(
            "pim",
            "localhost",
            credentials.username,
            credentials.password
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
                credentials.username,
                credentials.password,
                shopname = record[1],
                multibranch = record[2]
            )
        else:
            con = modules.database.mbinit(
                "pim",
                "localhost",
                credentials.username,
                credentials.password,
                record[1:-1]
            )
        
        person = record[0]
        modules.accounts.new_account(con, username, password)

    # main loop
    while True:
        if not record[2]:
            print(boxify(record[1].title(), width=swidth, align="centre"))

        elif person in record[4]:
            lwshop = record[4][person]
            print(boxify(record[1].title() + "-" + lwshop.title(), width=swidth, align="centre"))

        else:
            lwshop = askbranch(con)
            modules.shops.setlwshop(con, person, lwshop)

            data = modules.shops.fetchshops(con)
            record = [person]+[data[0], data[1], json.loads(data[2]), json.loads(data[3])]
            print(boxify(record[1].title() + "-" + lwshop.title(), width=swidth, align="centre"))

        followup = shopmenu()

        if followup == '1': # Adding an item
            addingitem(con)

        elif followup == "2": # Removing an item
            toremoveitem(con)

        elif followup == "5": # Manage shop option
            followup1 = manageshopmenu()

        elif followup == '4': # Insights
            pass

        elif followup == "3": # Inventory
            pass

        else:
            break
    
    #final steps
    modules.database.disconnect()

if __name__ == "__main__":
    main()