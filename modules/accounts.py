import modules.database as database

def getuserlist(con):
    # returns a list of all usernames.
    data = database.fetchtable(con, "credentials")
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
            database.insertrow(con, "credentials", record)

        return 1
    
    except ValueError:
        return 0  


def addtoshop(con, username, role, lwshop):
    # adds the passed use to members table
    database.insertrow(con, f"{lwshop}_members", (username, role))

def doespassmatch(con, provided_username, provided_password):
    # checks if the provided username matches with stored one.
    data = database.fetchtable(con, "credentials")

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