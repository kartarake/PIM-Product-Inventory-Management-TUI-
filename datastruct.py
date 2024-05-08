# credentials Document
credentials = {
    "username" : {
        "password" : "hashed password", #string
        "salt" : "salt", #string
    }
    # More of this...
}


# shop Document
shop = {
    "itemdata" : {
        "itemname" : {
            "quantity" : "no. of units (integer)",
            "price" : "price per unit (float)",
            "desc" : "Small desc of the item (string)"
        },
        # More of this...
    },

    "changes" : [
        ["itemname (string)", "changed count (integer)", "time (string)"],
        # More of this...
    ],

    "members" : {
        "username" : "role (string)",
        # More of this...
    }
}


# userdata Document
userdata = {
    "username" : {
        "lwshop" : "shopname (string)"
    },
    # More of this...
}