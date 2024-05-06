from modules.database import kardb
from modules.boxify import boxify

import modules.accounts

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

def createtable(db, name):
    try:
        db.createdoc(name)
    except NameError:
        pass

def main():
    # connecting to the mysql database
    db = kardb(
        "PIM",
        host = "localhost",
        user = credentials.username,
        passwd = credentials.password 
    )

    # creating tables
    createtable(db, "credentials")
    createtable(db, "shop")

    # app
    followup = landerpage()

    if followup == "signup":
        signup(db)
    elif followup == "login":
        login(db)
    else:
        sys.stderr.write("Login/Sign up neglected.")       
    
    #final steps
    db.disconnect()

if __name__ == "__main__":
    main()