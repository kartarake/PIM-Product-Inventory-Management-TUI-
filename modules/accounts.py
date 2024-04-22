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
    try:
        db.changedoc('credentials')
        data = db.data
        print(data)

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
    db.changedoc("credentails")
    userlist = list(db.data.keys())
    return userlist