import hashlib
import secrets
import database

def gensalt(n):
    charlist = list(range(48,58)) + list(range(65,91)) + list(range(97, 123))
    belt = list()
    for i in range(n):
        selected = secrets.choice(charlist)
        character = chr(selected)
        belt.append(character)
    salt = ''.join(belt)
    return salt


def hashmash(password, salt):
    salted_password = password.encode() + salt.encode()
    hashed_password = hashlib.sha256(salted_password).hexdigest()
    return hashed_password

def verifyhash(stored_password, provided_password, salt):
    hashed_password = hashmash(provided_password, salt)

    if hashed_password == stored_password:
        return True
    else:
        return False
    
def getuserlist(con):
    # returns a list of all usernames.
    data = database.fetchtable(con, "credentials")
    usernamelist = [row[0] for row in data]
    return usernamelist
    
def new_account(con, username, password):
    # use this to create new account in db.
    try:
        data = database.fetchtable(con, "credentials")
        usernamelist = getuserlist(con)

        if username in usernamelist:
            raise ValueError('Username already exists.')
        else:
            salt = gensalt(16)
            hashed_password = hashmash(password, salt)
            
            record = (username, hashed_password, salt)
            database.insertrow(con, "credentials", record)

        return 1
    
    except ValueError:
        return 0  

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
    salt = row[2]

    # returns true if password matches or returns false.
    return verifyhash(password, provided_password, salt)