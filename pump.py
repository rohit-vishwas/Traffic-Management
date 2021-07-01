from collections import *
from heapq import *
import mysql.connector
import math
mydb = mysql.connector.connect(host="localhost", user="root", password="1234")

cur = mydb.cursor()
cur.execute("use trafficManagementSystem")


def pathDFS(st_x, st_y, end_x, end_y, n, heights):  # return path and cost
    # defaultdict used
    graph = defaultdict(list)
    parent = defaultdict()
    # rows and columns
    rows, cols = len(heights), len(heights[0])
    for i in range(rows):
        for j in range(cols):
            moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for x, y in moves:
                pos_x, pos_y = i + x, j + y
                if 0 <= pos_x < rows and 0 <= pos_y < cols:
                    graph[(i, j)].append((heights[i][j], (pos_x, pos_y)))
                    graph[(pos_x, pos_y)].append(
                        (heights[pos_x][pos_y], (i, j)))

    # distance array
    dist = [[float('inf') for j in range(cols)] for i in range(rows)]
    start = (st_x, st_y)
    dist[start[0]][start[1]] = 0
    end = (end_x, end_y)
    pQueue = [(0, start)]

    while pQueue:
        cur_wt, cur_node = heappop(pQueue)
        # if current path looks shortest
        if dist[cur_node[0]][cur_node[1]] == cur_wt:

            # update for each neighbour
            for neigh_wt, neigh_node in graph[cur_node]:
                if cur_wt + neigh_wt < dist[neigh_node[0]][neigh_node[1]]:
                    dist[neigh_node[0]][neigh_node[1]] = cur_wt + neigh_wt
                    # push the updated node with its cost
                    heappush(pQueue, (cur_wt + neigh_wt, neigh_node))

                    parent[neigh_node] = cur_node
    path = [end]
    # print(parent)
    # path creation
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    # print(path)
    res = ""
    for i in range(1, len(path)):
        next_x, next_y = path[i]
        prev_x, prev_y = path[i-1]
        dif_x = next_x - prev_x
        dif_y = next_y - prev_y
        if dif_x == 1 and dif_y == 0:  # Path forming
            res += '4'                   # Move UP
        elif dif_x == -1 and dif_y == 0:
            res += '3'  # Move Down
        elif dif_x == 0 and dif_y == 1:
            res += '2'  # Move Right
        else:
            res += '1'  # Move Left
    return res


def query1(id):
    allDeliveryBoy = []
    cur.execute(
        """select ID from deliveryBoy where inuse <> 1 and pumpID = %d""" % id)
    for x in cur:
        allDeliveryBoy.append(x)
    return allDeliveryBoy


def query2():                       # Total messages came till now
    cur.execute("select * from informPetrolPump")
    messages = []
    for x in cur:
        messages.append(x)
    return messages


def query3(id):  # DeliveryBoy assign
    messages = query2()
    cur.execute("truncate table informPetrolPump")
    cur.execute("""select X, Y from petrolPump WHERE ID = %d""" % id)
    for x in cur:
        st_x, st_y = x[0], x[1]
    availDelivery = query1()
    for k in range(min(len(availDelivery), len(messages))):
        path = pathDFS(st_x, st_y, messages[k][2], messages[k][3])
        cur.execute("""UPDATE citizen SET X = %d, Y = %d, status = 1, path = '%s',fuel = %d, wallet = %d where id = %d""" % (
            st_x, st_y, str(path), 200, 10000, availDelivery[k]))
        cur.execute(
            """UPDATE deliveryBoy SET inuse = 1 where ID = %d""" % availDelivery[k])
    mydb.commit()


def petrolPump(id):
    global cur
    print("Welcome to the App")
    print("May I help you")
    while True:
        print("\n Choose Any \n")
        print("Query 1: Available deliverBoy \n Query 2: Check message \n Query 3: Assign delivery \n 4: Exit")
        choose = int(input())
        if choose == 4:
            break
        elif choose == 1:
            p = query1(id)
            print(len(p))
        elif choose == 2:
            msgs = query2()
            print("Total messages come ", len(msgs))
        elif choose == 3:
            query3(id)
