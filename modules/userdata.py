def fetchLWShop(db, person):
    db.changedoc("userdata")
    if not person in db.data:
        return None
    elif not 'lwshop' in db.data[person]:
        return None
    else:
        return db.data[person]["lwshop"]

def throwLWShop(db, person, shopname):
    db.changedoc("userdata")
    db.data[person]["lwshop"] = shopname
    db.savedoc()