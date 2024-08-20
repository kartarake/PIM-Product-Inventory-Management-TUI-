import unittest
from mysql.connector import connect

import modules.metrics

class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.con = connect(
            host = "localhost",
            user = "root",
            passwd = "mysql"
        )
        self.lwshop = "tn"

        cursor = self.con.cursor()
        cursor.execute("create database if not exists pim;")
        cursor.execute("use pim;")

        cursor.execute("""create table if not exists tn_itemdata (
            itemname varchar(30) primary key,
            quantity int,
            price float(10,4),
            description text
        )""")
        cursor.execute("""create table if not exists tn_changes (
            itemname varchar(30),
            ccount int,
            time datetime
        )""")

        cursor.execute("insert into tn_itemdata values ('a', 10, 10, 'a');")
        cursor.execute("insert into tn_itemdata values ('b', 10, 20, 'b');")
        cursor.execute("insert into tn_itemdata values ('c', 10, 30, 'c');")
        cursor.execute("insert into tn_itemdata values ('d', 10, 40, 'd');")
        cursor.execute("insert into tn_itemdata values ('e', 10, 50, 'e');")
        cursor.execute("insert into tn_itemdata values ('f', 10, 60, 'f');")
        cursor.execute("insert into tn_itemdata values ('g', 10, 70, 'g');")
        cursor.execute("insert into tn_itemdata values ('h', 10, 80, 'h');")
        cursor.execute("insert into tn_itemdata values ('i', 0, 90, 'i');")
        cursor.execute("insert into tn_itemdata values ('j', 0, 100, 'j');")

        cursor.execute("insert into tn_changes values ('a', 10, '2020-01-01 00:00:00');")
        cursor.execute("insert into tn_changes values ('b', 10, '2020-01-01 00:00:00');")
        cursor.execute("insert into tn_changes values ('c', 10, '2020-01-01 00:00:00');")
        cursor.execute("insert into tn_changes values ('d', 10, '2020-01-01 00:00:00');")
        cursor.execute("insert into tn_changes values ('e', 10, '2020-01-01 00:00:00');")
        cursor.execute("insert into tn_changes values ('f', 10, '2020-01-01 00:00:00');")
        cursor.execute("insert into tn_changes values ('g', 10, '2020-01-01 00:00:00');")
        cursor.execute("insert into tn_changes values ('h', 10, '2020-01-01 00:00:00');")
        cursor.execute("insert into tn_changes values ('i', 10, '2020-01-01 00:00:00');")
        cursor.execute("insert into tn_changes values ('i', -10, '2020-01-01 00:00:00');")
        cursor.execute("insert into tn_changes values ('j', 10, '2020-01-01 00:00:00');")
        cursor.execute("insert into tn_changes values ('j', -10, '2020-01-01 00:00:00');")

        self.con.commit()

    def tearDown(self) -> None:
        cursor = self.con.cursor()
        cursor.execute("drop database pim;")
        self.con.commit()
        self.con.close()

    def test_days(self):
        timestamp = "2020-01-01"
        days = modules.metrics.days(timestamp)
        self.assertEqual(days, 736936)

    def test_issameyear(self):
        year = 2020
        timestamp = "2020-01-01"
        sameyear = modules.metrics.issameyear(year, timestamp)
        self.assertEqual(sameyear, True)

    def test_invturnover(self):
        invturnover = modules.metrics.invturnover(self.con, self.lwshop)
        self.assertAlmostEqual(invturnover, 0.53, places=1)

    def test_stockoutrate(self):
        stockoutrate = modules.metrics.invstockout(self.con, self.lwshop)
        self.assertEqual(stockoutrate, 20.0)

if __name__ == "__main__":
    unittest.main()