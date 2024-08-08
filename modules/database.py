import mysql.connector as sql
import json

def init(dbname, host, user, password, shopname, multibranch):
    con = sql.connect(host=host, user=user, passwd=password)
    cursor = con.cursor()

    cursor.execute(f"create database if not exists {dbname};")
    cursor.execute(f"use {dbname}")

    cursor.execute("""create table if not exists shop (
                   shopname varchar(30) primary key,
                   multibranch int);""")
    
    record = (shopname, multibranch)
    cursor.execute(f"insert into shop values{record}")

    cursor.execute(f"""create table if not exists {None}_credentials (username varchar(30) primary key,
                   password varchar(64));""")
    
    cursor.execute(f"""create table if not exists {None}_itemdata (itemname varchar(30) primary key,
                   quantity int,
                   price float(10,4),
                   description text);""")
    
    cursor.execute(f"""create table if not exists {None}_changes (itemname varchar(30),
                   ccount int,
                   time datetime);""")
    
    cursor.execute(f"""create table if not exists {None}_members (
                   username varchar(30) primary key,
                   role varchar(30));""")
    
    con.commit()        
    return con

def mbinit(dbname, host, user, password, record):
    con = sql.connect(host=host, user=user, passwd=password)
    cursor = con.cursor()

    cursor.execute(f"create database if not exists {dbname};")
    cursor.execute(f"use {dbname}")

    cursor.execute("""create table if not exists shop (
                   shopname varchar(30) primary key,
                   multibranch int,
                   branchlist text,
                   trackers text);""")
    
    record = record + (json.dumps({}),)
    cursor.execute(f"insert into shop values{record};")

    cursor.execute(f"select branchlist from shop;")
    branchlist = json.loads(cursor.fetchone()[0])

    for branch in branchlist:
        cursor.execute(f"""create table if not exists {branch}_credentials (username varchar(30) primary key,
                    password varchar(64));""")
            
        cursor.execute(f"""create table if not exists {branch}_itemdata (itemname varchar(30) primary key,
                    quantity int,
                    price float(10,4),
                    description text);""")
            
        cursor.execute(f"""create table if not exists {branch}_changes (itemname varchar(30),
                    ccount int,
                    time datetime);""")
            
        cursor.execute(f"""create table if not exists {branch}_members (
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

def deleterow(con, table, where):
    cursor = con.cursor()
    cursor.execute(f"delete from {table} where {where}")
    con.commit()

def disconnect(con):
    con.close()