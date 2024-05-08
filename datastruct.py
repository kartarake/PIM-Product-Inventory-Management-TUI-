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
    "quantity" : {
        "itemname" : "quantity", #numbers
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