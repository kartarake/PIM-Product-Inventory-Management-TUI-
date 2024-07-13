# credentials Table
credentials = [
    ("username1 (varchar(30), primary key)", "password varchar(50)", "salt varchar(32)"), # row 1
    ("username2 (varchar(30), primary key)", "password varchar(50)", "salt varchar(32)"), # row 2
    ("username3 (varchar(30), primary key)", "password varchar(50)", "salt varchar(32)"), # row 3
    # More of this...
]


# itemdata Table
itemdata = [
    ("itemname1 (varchar(30) primary key)", "quantity (int)", "price (float(10,4))", "description (blob)"), # row 1
    ("itemname2 (varchar(30) primary key)", "quantity (int)", "price (float(10,4))", "description (blob)"), # row 2
    ("itemname3 (varchar(30) primary key)", "quantity (int)", "price (float(10,4))", "description (blob)"), # row 3
    # More of this...
]

# changes Table
changes = [
    ("itemname1 (varchar(30))", "ccount (int)", "time (datetime)"), # row 1
    ("itemname2 (varchar(30))", "ccount (int)", "time (datetime)"), # row 2
    ("itemname1 (varchar(30))", "ccount (int)", "time (datetime)"), # row 3
    # More of this...
]

# members Table
members = [
    ("username1 (varchar(30) primary key)", "role (varchar(30))"), # row 1
    ("username2 (varchar(30) primary key)", "role (varchar(30))"), # row 2
    ("username3 (varchar(30) primary key)", "role (varchar(30))"), # row 3
    # More of this...
]