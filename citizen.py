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
    return res, dist[end[0]][end[1]], dist


def query1(id, grid, n):
    print("Enter destination cordinate")
    x, y = map(int, input().strip().split())
    cur.execute(
        """SELECT X, Y FROM citizen WHERE ID = %d""" % id)
    strt = list(cur)
    x1, y1 = strt[0][0], strt[0][1]
    print("start ", x1, y1, "dest", x, y)
    path1, cost1, dist = pathDFS(x1, y1, x, y, n, grid)
    # print(path, cost)
    # print(dist)
    cost2, path2 = 0, ""
    if x1 < x:
        for j in range(x1, x):
            cost2 += grid[j][y1]
            path2 += "2"
    elif x1 > x:
        for j in range(x1, x, -1):
            cost2 += grid[j][y1]
            path2 += "1"
    if y1 < y:
        for j in range(y1, y):
            cost2 += grid[x][j]
            path2 += "3"
    elif y1 > y:
        for j in range(y1, y, -1):
            cost2 += grid[x][j]
            path2 += "4"
    print("Choose path number:")
    print("Path 1 : Fastest path cost : ", cost2)
    print("Path 2 : Cheapest path cost : ", cost1)
    choose = int(input())
    if choose == 1:
        cur.execute(
            """UPDATE citizen SET status = 1, path = '%s' where id = %d""" % (str(path2), int(id)))
    else:
        cur.execute(
            """UPDATE citizen SET status = 1, path = '%s' where id = %d""" % (str(path1), int(id)))
    mydb.commit()


def query2(id):                       # Fuel at any instant
    cur.execute("select fuel from citizen WHERE ID = %d" % id)
    for x in cur:
        return x[0]


def query3(id):  # Wallet value
    cur.execute("""select wallet from citizen WHERE ID = %d""" % (id))
    for x in cur:
        return x[0]


def query4(id):    # Position of citizen
    cur.execute("""select X, Y from citizen WHERE ID = %d""" % id)
    for x in cur:
        return x[0], x[1]


def moveMent(x, y, move):
    print("@@@@@@@########  ", x, y, move, " #####")
    if move == '1':
        return x-1, y
    elif move == '2':
        return x+1, y
    elif move == '3':
        return x, y-1
    else:
        return x, y + 1


def query5(id):     # Inform Hospital
    x_pos, y_pos = query4(id)
    cur.execute("select ID, X,Y from hospital where availBed > 0")
    hospitalArr = []
    for x in cur:
        hospitalArr.append(x)
    x_inf, y_inf = 0, 0
    if len(hospitalArr) == 0:
        print("So sad! No Hospital in this city")
    else:
        cst, hostID = float('inf'), 0
        for k in hospitalArr:
            if abs(k[1] - x_pos) + abs(k[2] - y_pos) < cst:
                cst = abs(k[1] - x_pos) + abs(k[2] - y_pos)
                hostID = k[0]
        cur.execute("insert into callHospital (citizenID, hospitalID, X,Y) values (%d,%d,%d,%d)" % (
            id, hostID, x_pos, y_pos))
    mydb.commit()


def query6(id, n, grid):    # Inform Petrol Pump
    x_pos, y_pos = query4(id)  # current position
    fuel, wallet = query2(id), query3(id)      # Fuel, Wallet
    cur.execute("""select path from citizen WHERE ID = %d""" % id)
    for x in cur:
        path = x[0]
    cur.execute("select ID, X,Y from petrolPump")
    pumpArr = []
    for x in cur:
        pumpArr.append(x)  # List of all pump in the city
    if fuel >= len(path):
        print("You have enough fuel to reach your destination")
    else:
        x, y = x_pos, y_pos
        checkPathArr, finalID, deliveryCost = [[x, y]], 0, float('inf')
        for k in range(len(path)):
            x, y = moveMent(x, y, path[k])
            if len(checkPathArr) <= fuel:
                # All vertex in a given path with available fuel
                checkPathArr.append([x, y])
        dest_X, dest_Y = x, y  # Destination co-ordinate
        pathVAlue = [0, 0]
        # print(checkPathArr, "####")
        # nearestPumpCost function will give cheapest petrol pump ID at given point

        def nearestPumpCost(x_check, y_check):
            pth, cost, dist = pathDFS(x_check, y_check, 0, 0, n, grid)
            pumpSelectedID, cst = 0, float('inf')
            for k in pumpArr:
                if dist[k[1]][k[2]] < cst:
                    cst = dist[k[1]][k[2]]
                    pumpSelectedID = k[0]
            return cst, pumpSelectedID
        for k in checkPathArr:  # Check cheapest petrol pump reach from all reachable path
            tempCost, tempID = nearestPumpCost(k[0], k[1])
            pump1_X, pump1_Y = 0, 0  # this is our desired petrol pump
            if tempCost < deliveryCost:
                deliveryCost = 2 * tempCost
                finalID = tempID
                pump1_X, pump1_Y = k[0], k[1]
                pathVAlue = k
        # cost2, pumpID2 will be used when we opted to go petrol pump first
        cost2, pumpID2 = nearestPumpCost(x_pos, y_pos)
        cur.execute(
            """select X,Y from petrolPump where ID = %d""" % pumpID2)
        tmpp = []
        for xp in cur:
            tmpp = xp
        # Co-rdinate of direct petrolpump
        pumpID2_X, pumpID2_Y = tmpp[0], tmpp[1]
        # Path, Cost to go from current position to nearest Petrol Pump
        pth1, cst1, dist1 = pathDFS(
            x_pos, y_pos, pumpID2_X, pumpID2_Y, n, grid)
        # Path, Cost to go from nearest Petrol Pump to destination
        pth2, cst2, dist2 = pathDFS(
            pumpID2_X, pumpID2_Y, dest_X, dest_Y, n, grid)
        cost1 = cst1 + cst2  # Total cost needed to go through petrol pump
        # costt is a total cost to reaching at destination without going through petrol pump
        costt = dist1[dest_X][dest_Y] + deliveryCost + \
            (abs(pump1_X - pathVAlue[0]) + abs(pump1_Y - pathVAlue[1])) * 10
        choose = 2
        if fuel >= len(pth1):
            print("Choose option")
            print("Choose 1: If you want to visit nearest petrolpump before destination now. Then you have to pay amount",
                  cost1, "for reaching at destination")
            print(
                "Choose 2: If you want to get fuel in current path then you have to pay amount", costt, " To reaching at destination")
            choose = int(input())
        else:
            print(
                "You have not enough fuel to visit nearest petrol pump, we order fuel from nearest petrolpump")
        print("How much fuel you want to order")
        fuelAmt = int(input())
        if choose == 1:
            newPath = pth1 + pth2
            ful, wall = fuel+fuelAmt, wallet - fuelAmt * 10
            cur.execute("""UPDATE citizen SET status = 1, path = '%s',fuel = %d, wallet = %d where id = %d""" % (
                str(newPath), int(ful), int(wall), int(id)))
        else:
            cur.execute("insert into informPetrolpump (citizenID, pumpID, X,Y, fuelAmount) values (%d,%d,%d,%d,%d)" % (
                id, finalID, pump1_X, pump1_Y, fuelAmt))
    mydb.commit()


def query7(id):  # Start your vehicle
    cur.execute("""UPDATE citizen SET status = 1 where id = %d""" % int(id))
    mydb.commit()


def query8(id):  # Stop your vehicle
    cur.execute("""UPDATE citizen SET status = 0 where id = %d""" % int(id))
    mydb.commit()


def citizen(id):
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
        print("Query 1: Give me path \n Query 2: My fuel \n Query 3: My wallet \n Query 4: My position \n Query 5: inform Hospital \n Query 6: Need fuel \n Query 7: Start Moving \n Query 8: Stop Moving \n Querry 9: Exit")
        choose = int(input())
        if choose == 9:
            break
        elif choose == 1:
            query1(id, grid, n)
        elif choose == 2:
            fuel = query2(id)
            print("Available fuel ", fuel)
        elif choose == 3:
            wallet = query3(id)
            print("Your Wallet ", wallet)
        elif choose == 4:
            x_pos, y_pos = query4(id)
            print("Your current Position X: ", x_pos, " Y: ", y_pos)
        elif choose == 5:
            query5(id)
        elif choose == 6:
            query6(id, n, grid)
        elif choose == 7:
            query7(id)
        else:
            query8(id)


citizen(4)
