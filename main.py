from modules.database import kardb
from modules.boxify import boxify

import modules.accounts
import modules.database
import modules.userdata
import modules.shops

import credentials
import sys

# Variable Dashboard
swidth = 170


def landerpage(): # The first page upon opening the application.
    str1 = """
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
    
def signup(db): # The page where they can sign up an account.
    print(boxify("Sign Up", width = swidth))
    while True:
        username = input("Enter username:")
        l1 = modules.accounts.getuserlist(db)
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
    
    modules.accounts.new_account(db,username,password)
    return username

def login(db):
    print(boxify("Login", width = swidth))
    while True:
        username = input("Enter username : ")
        l1 = modules.accounts.getuserlist(db)
        if username in l1:
            break
        else:
            print(boxify("The given username does not exist", width = swidth))
    while True:
        password = input("Enter password : ")
        valuepassword = modules.accounts.doespassmatch(db,username,password)
        if valuepassword == True:
            break
        else:
            print(boxify("The given password is incorrect", width = swidth))
    return username

def mainmenu(db, person):
    print(boxify("Main Menu",width = swidth ,align = "centre"))
    lwshop = modules.userdata.fetchLWShop(db, person)
    str1 = f"[1] Previous shop - {lwshop}   |   [2] Other shops    |   [3] Exit"
    print(boxify(str1,width = swidth ,align = "centre"))
    while True:
        choice = input('Enter respective choice to continue : ')
        if choice in ('1', '2','3','Previous shop','Manage shop','Exit'):
            break
        else:
            print(boxify('Invalid choice', width = swidth, align = "centre"))
    
    if choice == 'Previous shop':
        choice = '1'
    elif choice == 'Manage shop':
        choice = '2'
    elif choice == 'Exit':
        choice = '3'
    else:
        pass

    return choice

def shopmenu():
    str1 = "[1] Add item    |    [3] Remove item     |    [3] Insights     |   [4] Manage shop"
    print(boxify(str1,width = swidth,align = "centre"))
    while True:
        choice = input('Enter respective choice to continue : ')
        if choice in ('1', '2','3','4','Add item','Insights','Manage shop','Remove item'):
            break
        else:
            print(boxify('Invalid choice', width = swidth, align = "centre"))
    
    if choice == "Add item":
        choice = '1'
    elif choice == 'Remove item':
        choice = '2'
    elif choice == 'Insights':
        choice = '3'
    elif choice == 'Manage shop':
        choice = '4'
    else:
        pass

    return choice

def addingitem(db, shopname):
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
    desc = '\n'.join(para)
    if desc == '':
        desc = None

    modules.shops.newitem(db, shopname, itemname, price, desc)
    modules.shops.additem(db, shopname, itemname, quantity)

def createtable(db, name):
    try:
        db.createdoc(name)
    except NameError:
        pass

def toremoveitem(db,shopname):
    while True:
        itemname = input("Enter itemname:")
        itemlist = modules.shops.fetchitemlist(db,shopname)
        if itemname not in itemlist:
            print("The given item is not in the shop")
        else:
            break
    
    while True:
        quantity = int(input("Enter the no. of items to remove:"))
        actualquantity = modules.shops.fetchitemquantity(db, shopname, itemname)
        if quantity > actualquantity:
            print("The given amount is greater than the amount of items in the shop")
        else:
            break    

    modules.shops.removeitem(db, shopname, itemname, count = quantity)

def manageshopmenu():
    str1 = "[1] Change shopname    |    [2] Permissions    |    [3] Export log    |   [4] Back"
    print(boxify(str1,width = swidth,align = "centre"))
    while True:
        choice = input('Enter respective choice to continue : ')
        if choice.lower() in ('1', '2','3','4','change shopname','permissions','export log','back'):
            if choice.lower() == "change shopname":
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

def main():
    # connecting to the mysql database
    try:
        con = modules.database.connect()
    except Exception:
        con = modules.database.init()

    # app
    followup = landerpage()

    if followup == "signup":
        person = signup(db)
    elif followup == "login":
        person = login(db)
    else:
        sys.stderr.write("Login/Sign up neglected.")
    del followup      

    while True:
        followup = mainmenu(db, person)
        if followup == '1':
            if not modules.userdata.fetchLWShop(db, person):
                print(boxify('You have no last working shop. Please create/open from manage shop option', width=swidth))
                continue
            else:
                shopname = modules.userdata.fetchLWShop(db, person)
                followup1 = shopmenu()
                if followup1 == '1':
                    addingitem(db,shopname)
                elif followup1 == "2":
                    toremoveitem(db, shopname)
                elif followup1 == "4":
                    followup2 = manageshopmenu()
        elif followup == '2':
            pass
        else:
            break
    
    #final steps
    db.disconnect()

if __name__ == "__main__":
    main()