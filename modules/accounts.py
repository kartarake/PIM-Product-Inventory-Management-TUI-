import hashlib
import secrets

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
    
def new_account(db, username, password):
    # use this to create new account in db.
    try:
        db.changedoc('credentials')
        data = db.data

        if username in data:
            raise ValueError('Username already exists.')
        else:
            salt = gensalt(16)
            hashed_password = hashmash(password, salt)

            usercreds = {
                "password":hashed_password,
                "salt":salt
            }

            db.updatedoc(branch = {username:usercreds})

        return 1
    
    except ValueError:
        return 0
    
def getuserlist(db):
    # returns a list of all usernames.
    db.changedoc("credentials")
    userlist = list(db.data.keys())
    return userlist

def doespassmatch(db, provided_username, provided_password):
    # checks if the provided username matches with stored one.
    db.changedoc("credentials")
    data = db.data

    if not(provided_username in getuserlist(db)):
        raise ValueError("Username not in data")
    else:
        pass

    password = data[provided_username]["password"]
    salt = data[provided_username]["salt"]

    # returns true if password matches or returns false.
    return verifyhash(password, provided_password, salt)