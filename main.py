from modules.database import kardb

import modules.accounts

import credentials

def main():
    # connecting to the mysql database
    db = kardb(
        "PIM",
        host = "localhost",
        user = credentials.username,
        passwd = credentials.password 
    )

    # creating tables
    print(db.getdoclist())
    try:
        db.createdoc("credentials")
    except NameError:
        pass

    # app
    modules.accounts.new_account(db, "kar", "abcd")
    
    db.disconnect()

if __name__ == "__main__":
    main()