from collections import *
from heapq import *
import mysql.connector
import math
mydb = mysql.connector.connect(host="localhost", user="root", password="1234")

cur = mydb.cursor()
cur.execute("use trafficManagementSystem")


def query1(x, y):
    pass


def query2(x, y):
    pass


def query3(x, y):
    pass


def query4(x, y):
    pass


def query5(x, y):
    pass


def query6(x, y):
    pass


def query7(x, y):
    pass


def query8(x, y):
    pass


def query9():
    pass


def movement():
    pass


def police(id):
    global cur
    cur.execute("select * from location")
    cur1 = list(cur)
    n = int(math.sqrt(len(cur1)))
    grid = [[0 for k in range(n)] for k in range(n)]
    for k in cur1:
        grid[k[0]][k[1]] = k[2]
    # print(grid, n)
    print("Welcome to the App")
    print("May I help you")
    while True:
        print("\n Choose Any \n")
        print("Query 1: total east moving count \n Query 2: total west moving count \n Query 3: total south moving count \n Query 4: total north moving count \n Query 5: Open East \n Query 6: Open West \n Query 7: Open south \n Query 8: Open north \n Querry 9: Total wallet value \n Querry 10: Exit")
        choose = int(input())
        if choose == 10:
            break
        elif choose == 1:
            east = query1(x, y)
            print("Total east moving vehicles count", east)
        elif choose == 2:
            west = query2(x, y)
            print("Total west moving vehicles count", west)
        elif choose == 3:
            south = query3(x, y)
            print("Total south moving vehicles count", south)
        elif choose == 4:
            north = query4(x, y)
            print("Total north moving vehicles count", north)
        elif choose == 5:
            query5(x, y)
        elif choose == 6:
            query6(x, y)
        elif choose == 7:
            query7(x, y)
        elif choose == 8:
            query8(x, y)
        else:
            wallet = query9(x, y)
            print("Your wallet value :", wallet)


police(4)
