from collections import *
from heapq import *
import mysql.connector
import math
mydb = mysql.connector.connect(host="localhost", user="root", password="1234")

cur = mydb.cursor()
cur.execute("use trafficManagementSystem")

print("Welcome to this app")
print("Enter your ID")
id = int(input())
print("Enter your role")
role = int(input())
cur.execute(
    """select password from logIN where ID = %d and role = %d""" % (id, role))
for x in cur:
    pas = x[0]
while True:
    print("Enter your password")
    passw = input().strip()
    if pas == passw:
        print("You successfully LogIN")
        print("We will help you in managing time during traffic")
        if role == 1:
            citizen(id)
        elif role == 2:
            hospital(id)
        elif role == 3:
            petrolPump(id)
        else:
            pump(id)
        break
