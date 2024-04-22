from modules.database import kardb
from modules.boxify import boxify

import modules.accounts

import credentials


def landerpage():
    str1 = """
    __        _______ _     ____ ___  __  __ _____   _____ ___    ____ ___ __  __ 
    \ \      / / ____| |   / ___/ _ \|  \/  | ____| |_   _/ _ \  |  _ \_ _|  \/  |
     \ \ /\ / /|  _| | |  | |  | | | | |\/| |  _|     | || | | | | |_) | || |\/| |
      \ V  V / | |___| |__| |__| |_| | |  | | |___    | || |_| | |  __/| || |  | |
       \_/\_/  |_____|_____\____\___/|_|  |_|_____|   |_| \___/  |_|  |___|_|  |_|
    """
    print(boxify(str1,width = 170, align="centre"))
    str2 = "[1] Login      |      [2] Sign up"
    print(boxify(str2,width = 170, align="centre"))

    while True:
        choice = input('Enter respective number to continue : ')

        if choice in ('1', '2','login','signup'):
            break
        else:
            print(boxify('Invalid choice', width = 170, align = "centre"))

    if choice in ('1', 'login'):
        return 'login'
    else:
        return 'signup'

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

    # app
    followup = landerpage()
    
    #final steps
    db.disconnect()

if __name__ == "__main__":
    main()