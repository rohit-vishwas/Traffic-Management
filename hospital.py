from collections import *
from heapq import *
import mysql.connector
import math
mydb = mysql.connector.connect(host="localhost", user="root", password="1234")

cur = mydb.cursor()
cur.execute("use trafficManagementSystem")


def fastestPath(x1, y1, x, y):
    path2 = ""
    if x1 < x:
        for j in range(x1, x):
            path2 += "2"
    elif x1 > x:
        for j in range(x1, x, -1):
            path2 += "1"
    if y1 < y:
        for j in range(y1, y):
            path2 += "3"
    elif y1 > y:
        for j in range(y1, y, -1):
            path2 += "4"
    return path2


def query1(id):
    cur.execute(
        """SELECT availBed FROM hospital WHERE ID = %d""" % id)
    for x in cur:
        return x


def query2():                       # Total messages came till now
    cur.execute("select * from callHospital")
    messages = []
    for x in cur:
        messages.append(x)
    return messages


def query3(id):  # Ambulance assign
    messages = query2()
    cur.execute("truncate table callHospital")
    cur.execute("""select X, Y, availBed from hospital WHERE ID = %d""" % id)
    for x in cur:
        st_x, st_y, cnt = x[0], x[1], x[2]
    cur.execute("""select ID from ambulance WHERE hospitalID = %d""" % (id))
    availAmbulances = []
    for x in cur:
        availAmbulances.append(x[0])
    print(availAmbulances, messages)
    for k in range(min(len(availAmbulances), len(messages))):
        path = fastestPath(st_x, st_y, messages[k][2], messages[k][3])
        cur.execute("""UPDATE citizen SET X = %d, Y = %d, status = 1, path = '%s',fuel = %d, wallet = %d where id = %d""" % (
            st_x, st_y, str(path), 200, 10000, availAmbulances[k]))
        cnt -= 1
        cur.execute(
            """UPDATE hospital SET availBed = %d where id = %d""" % (cnt, id))
    mydb.commit()


def hospital(id):
    global cur
    print("Welcome to the App")
    print("May I help you")
    while True:
        print("\n Choose Any \n")
        print("Query 1: Available Bed count \n Query 2: Check message \n Query 3: Assign Ambulance \n 4: Exit")
        choose = int(input())
        if choose == 4:
            break
        elif choose == 1:
            query1(id)
        elif choose == 2:
            msgs = query2()
            print("Total messages come ", len(msgs))
        elif choose == 3:
            query3(id)


hospital(1)
