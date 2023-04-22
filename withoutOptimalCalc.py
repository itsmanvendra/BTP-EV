import math
import random
import sys
from math import ceil, floor
import numpy as np
import pandas as pd
import itertools
import csv
import matplotlib.pyplot as plt

swapTime = 600      #seconds per vehicle
GridX = 10000       #meters
GridY = 10000       #meters
intervalOfChargingStations = 2000       #meters
noOfRequests = 150      #per hour
numberOfChargingStations = GridX*GridY//intervalOfChargingStations**2
int_min_speed=20    #kmph
int_max_speed=40    #kmph
high_min_speed=60   #kmph
high_max_speed=80   #kmph
startTime = 0

################################################################################################################

ChargingStationCode = []
CSx = []
CSy = []
occupancyTime=[]
averageActulTime=[]
noOfCars=[]
destX=[]
destY=[]
randomTime=[]
randomX=[]
randomY=[]
allocatedCS=[]
arrivalTime=[]
final_ans = []
semifinalans = []
final_ans_distance = []
final_ans_waitTime = []



def delta(n):
    return n//10

def vehicleDensity(time):
    if time >= 0 and time < 6:
        return noOfRequests - 2 * delta(noOfRequests)
    elif time >= 6 and time < 8:
        return noOfRequests - delta(noOfRequests)
    elif time >= 8 and time < 11:
        return noOfRequests + delta(noOfRequests)
    elif time >=11 and time < 13:
        return noOfRequests
    elif time >=13 and time < 16:
        return noOfRequests - delta(noOfRequests)
    elif time >=16 and time < 18:
        return noOfRequests
    elif time >=18 and time < 21:
        return noOfRequests + delta(noOfRequests)
    else:
        return noOfRequests - delta(noOfRequests)


def makeZero(array):
    for i in range(len(array)):
        array[i]=0

def restart():
    global randomTime 
    randomTime=[]
    global randomX
    randomX=[]
    global randomY
    randomY=[]
    global allocatedCS
    allocatedCS=[]
    global arrivalTime
    arrivalTime=[]

def makeStations(GridX,GridY,intervalOfChargingStations):
    for i in range(0,GridX,intervalOfChargingStations):
        for j in range(0,GridY,intervalOfChargingStations):
            name = "CS"+str(i//1000)+str(j//1000)
            ChargingStationCode.append(name)
            CSx.append(i)
            CSy.append(j)
            occupancyTime.append(0)
            averageActulTime.append(0)
            noOfCars.append(0)

def generateRequest(startTime,GridX,GridY,noOfRequests):
    for i in range(noOfRequests):
        randomTime.append(random.randint(startTime,3600+startTime))
        randomX.append(random.randint(0,GridX))
        randomY.append(random.randint(0,GridY))
        destX.append(random.randint(0,GridX))
        destY.append(random.randint(0,GridY))
        allocatedCS.append(0)
        arrivalTime.append(0)
    randomTime.sort()

def distanceBetweenAB(A,B):
    hor_dis=abs(A[0]-B[0])
    ver_dis=abs(A[1]-B[1])
    return hor_dis + ver_dis

def findNearestHighway(A,B):
    A1 = []
    x1 = A[0]
    y1 = A[1]
    x2 = B[0]
    y2 = B[1]
    if x2>x1:
        vert_highway=ceil(x1/1000)*1000
    else:
        vert_highway=floor(x1/1000)*1000
    if y2>y1:
        horiz_highway=ceil(y1/1000)*1000
    else:
        horiz_highway=floor(y1/1000)*1000
    horHigPointA=[x1,horiz_highway]
    verHigPointA=[vert_highway,y1]

    #for A
    if distanceBetweenAB(A,horHigPointA) < distanceBetweenAB(A,verHigPointA):
        A1.append(x1)
        A1.append(horiz_highway)
    else:
        A1.append(vert_highway)
        A1.append(y1)
    return A1

def timeToTravel(A,B):
    Nearest_Highway_pointA = findNearestHighway(A,B)[:]
    high_distance = distanceBetweenAB(Nearest_Highway_pointA,B)
    int_distanceA = distanceBetweenAB(A,Nearest_Highway_pointA)
    highway_speed = (random.randint(high_min_speed,high_max_speed)*5)/18
    interior_speed = (random.randint(int_min_speed,int_max_speed)*5)/18
    high_time = high_distance/highway_speed
    inter_time = int_distanceA/interior_speed
    travel_time = high_time + inter_time
    travel_time  = round(travel_time,2)
    return travel_time

def waitingTime(arrivalTime,currentOccupancyTime,pastComputedTime,weightage):
    pastWeightage = weightage
    currentWeightage = 1 - pastWeightage
    if arrivalTime > currentOccupancyTime:
        return currentWeightage * (0) + pastWeightage * (pastComputedTime)
    else:
        currentWaitTime =  currentOccupancyTime - arrivalTime
        return currentWeightage * (currentWaitTime) + pastWeightage * (pastComputedTime)

# def findOptimalCS(pastData,weightage,reqTime,reqX,reqY):
#     A = [reqX,reqY]
#     tmp = sys.maxsize
#     ans = []
#     for i in range(numberOfChargingStations):
#         B = [CSx[i],CSy[i]]
#         c = distanceBetweenAB(A,B)
#         if c > 5000:
#             continue
#         tt = timeToTravel(A,B)
#         wt = waitingTime(reqTime + tt,occupancyTime[i],pastData[i],weightage)
#         if tt + wt < tmp:
#             ans = [i, tt, wt]
#             tmp = tt + wt
#     return ans


def findnearestCS(reqTime, reqX, reqY):
    A = [reqX, reqY]
    tmp = sys.maxsize
    ans = []
    for i in range(numberOfChargingStations):
        B = [CSx[i], CSy[i]]
        tt = timeToTravel(A,B)
        wt = waitingTime(reqTime+tt, occupancyTime[i], 0, 0)
        if tt < tmp:
            tmp = tt
            ans = [i, tt, wt]
    return ans


totalTime=[]
waitTime = []
distanceWise = []

def solveRequests(noOfRequests):
 
    
    global totalTime
    global waitTime
    global distanceWise

    for i in range(noOfRequests):
        nearestCS = findnearestCS(randomTime[i],randomX[i],randomY[i])
        ind = nearestCS[0]
        tt =  nearestCS[1]
        wt = nearestCS[2]
        Z = [destX[i],destY[i]]
        
        
        X = [randomX[i],randomY[i]]
        Y = [CSx[ind],CSy[ind]]
        timeToDest = timeToTravel(Z,Y)
        totalTime1 = round(tt+wt+600+timeToDest,2)
        distanceWise.append(distanceBetweenAB(X,Y)+distanceBetweenAB(Y,Z))
        waitTime.append(wt)
        totalTime.append(totalTime1)
        


        noOfCars[ind] += 1
        occupancyTime[ind] = randomTime[i] + tt + wt + swapTime
        averageActulTime[ind] = ( (noOfCars[ind] - 1)*averageActulTime[ind] + wt ) / noOfCars[ind]
        allocatedCS[i] = ChargingStationCode[ind]
        
        arrivalTime[i] = randomTime[i] + tt
    
makeStations(GridX,GridY,intervalOfChargingStations)

# generateRequest(startTime,GridX,GridY,noOfRequests)

# solveRequests()

# #Store Co-ordinates of Charging Stations corresponding to their Code.
# df1 = pd.DataFrame({'ChargingStationCode':ChargingStationCode, 'CSx':CSx, 'CSy':CSy,'Occupancy Time':occupancyTime,'Average Actual Time':averageActulTime,'Cars':noOfCars})
# df1.to_csv('ChargingStationsList.csv', index=False)

# #Store Co-ordinates of all requests corresponding to their time.
# df = pd.DataFrame({'Time' : randomTime, 'X': randomX, 'Y' : randomY,'allocated Charging Station':allocatedCS,'arrival Time':arrivalTime})
# df.to_csv('All_Requests.csv', index = False)

df2 = pd.DataFrame({'ChargingStationCode':ChargingStationCode})
df2.to_csv('datasetWithoutOptimization.csv',index=False)
df2=pd.read_csv('datasetWithoutOptimization.csv')

# for i in range(24):
#         requests = vehicleDensity(i)
#         generateRequest(startTime + (i*3600),GridX,GridY,requests)
#         solveRequests(requests)
#         z='AverageTime'+str(i)+"(seconds)"
#         df2.insert(i+1,z,averageActulTime)
#         makeZero(averageActulTime)
#         makeZero(noOfCars)
#         restart()
# df2.to_csv('Hourly Data.csv',index=False)

# def generateHourlyData(day):

#     if day==0:
#         for i in range(24):
#             requests = vehicleDensity(i)
#             generateRequest(startTime + (i*3600),GridX,GridY,requests)
#             pastData = [0] * 25
#             solveRequests(pastData,requests,day/10)
#             z='AverageTime'+str(i)+"(seconds)"
#             df2.insert(i+1,z,averageActulTime)
#             makeZero(averageActulTime)
#             makeZero(noOfCars)
#             restart()

#     else:
#         if day >= 7:
#             day = 7
#         elif day >= 20:
#             day = 8
#         for i in range(24):
#             requests = vehicleDensity(i)
#             z='AverageTime'+str(i)+"(seconds)"
#             pastData = df2[z].tolist()
#             generateRequest(startTime + (i*3600),GridX,GridY,requests)
#             solveRequests(pastData,requests,day/10)
#             df2[z] = averageActulTime
#             makeZero(averageActulTime)
#             makeZero(noOfCars)
#             restart()
#     makeZero(occupancyTime)
#     df2.to_csv('datasetWithOptimization.csv',index=False)

# for i in range(10):
#     # generateHourlyData(i)



def initiliaze(requests):
    for i in range(requests):
        semifinalans.append(0)
        allocatedCS.append(0)
        arrivalTime.append(0)

# df2=pd.read_csv('datasetWithoutOptimization.csv')
df = pd.read_csv('newrandomdata.csv')
for x in range(24):
    requests = vehicleDensity(x)
    initiliaze(requests)
    totalTime = []
    
    waitTime =[]
    distanceWise=[]
    # z='AverageTime'+str(x)+"(seconds)"
    # pastData = df2[z].tolist()
    
    m = 'randomTime'+str(x)+'(seconds)'
    n = 'randomX'+str(x)+'(meters)'
    o = 'randomY'+str(x)+'(meters)'
    # p = 'soc'+str(x)
    # q = 'batteryCapacityUser'+str(x)+'(kwh)'
    # r = 'ecrUser'+str(x)+'(kwh/km)'
    s = 'destX'+str(x)+'(meters)'
    t = 'destY'+str(x)+'(meters)'
    randomTime = df[m].tolist()[:requests]
    randomX = df[n].tolist()[:requests]
    randomY = df[o].tolist()[:requests]
    # soc = df[p].tolist()[:requests]
    # batteryCapacityUser = df[q].tolist()[:requests]
    # ecrUser = df[r].tolist()[:requests]
    destX = df[s].tolist()[:requests]
    destY = df[t].tolist()[:requests]
    # print("hhi",randomY)
    solveRequests(requests)
    # print(len(sams), requests)
    final_ans_waitTime.append(waitTime)
    final_ans_distance.append(distanceWise)
    final_ans.append(totalTime)
    semifinalans = []
    allocatedCS = []
    arrivalTime = []
    
    makeZero(averageActulTime)
    makeZero(noOfCars)
    restart()
df999 = pd.DataFrame({'withoutOptimization':final_ans})
df999.to_csv('withoutOptimization.csv',index=False)
# pprint("hhi",randomY)rint(randomY)
# print("hhi")
# print(randomY)
df969 = pd.DataFrame({'withoutOptimizedDist':final_ans_distance})
df969.to_csv('withoutOptimizedDist.csv',index=False)

df1999 = pd.DataFrame({'withoutOptimizedTime':final_ans_waitTime})
df1999.to_csv('withoutOptimizedTime.csv',index=False)
# xxxx = final_ans[10]
# xaxis = np.arange(0, len(xxxx), 1) 
# plt.plot(xaxis, xxxx)
# plt.show()

