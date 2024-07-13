import mysql.connector as sql

def init(dbname, host, user, password):
    con = sql.connect(host=host, user=user, passwd=password)
    cursor = con.cursor()

    cursor.execute(f"create database if not exists {dbname};")
    cursor.execute(f"use {dbname}")

    cursor.execute("""create table if not exists credentials (username varchar(30) primary key,
                   password varchar(50),
                   salt varchar(32));""")
    
    cursor.execute("""create table if not exists itemdata (itemname varchar(30) primary key,
                   quantity int,
                   price float(10,4),
                   desc blob);""")
    
    cursor.execute("""create table if not exists changes (itemname varchar(30),
                   ccount int,
                   time datetime);""")
    
    cursor.execute("""create table if not exists members (
                   username varchar(30) primary key,
                   role varchar(30));""")
    
    return con
    
def connect(dbname, host, user, password):
    con = sql.connect(host=host, user=user, passwd=password, database=dbname)
    return con

def fetchtable(con, table):
    cursor = con.cursor()
    cursor.execute(f"select * from {table};")
    data = cursor.fetchall()
    return data

def puttable(con, table, grid):
    cursor = con.cursor()
    cursor.execute(f"delete from {table};")
    
    for row in grid:
        row = tuple(row)
        cursor.execute(f"insert into {table} values{row};")

    con.commit()

def insertrow(con, table, row):
    row = tuple(row)

    cursor = con.cursor()
    cursor.execute(f"insert into {table} values{row};")
    con.commit()