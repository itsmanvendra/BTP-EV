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
soc = []
batteryCapacity = [22, 22.5, 23, 26.5, 27, 29, 29.5, 30, 31.5,32] #// 22kwh to 32kwh
energyConsumptionRate = [0.16, 0.165, 0.17, 0.18, 0.185, 0.19, 0.195, 0.2, 0.205, 0.21] #// 0.16 to 0.21
batteryCapacityUser = []
ecrUser = []
destX = []
destY = []
occupancyTime=[]
averageActulTime=[]
noOfCars=[]

randomTime=[]
randomX=[]
randomY=[]
allocatedCS=[]
arrivalTime=[]
final_ans = []
semifinalans = []
final_ans_distance = []
final_ans_waitTime = []
final_ans_distanceCSToDest = []


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
        soc.append(random.uniform(0.03,0.06))
        destX.append(random.randint(0,GridX))
        destY.append(random.randint(0,GridY))
        batteryCapacityUser.append(random.choice(batteryCapacity))
        ecrUser.append(random.choice(energyConsumptionRate))
        allocatedCS.append(0)
        arrivalTime.append(0)
    randomTime.sort()


def computeSOC(soc,batteryCapacityUser,ecrUser):
    return (soc*batteryCapacityUser/ecrUser)*1000

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
    # highway_speed = (random.randint(high_min_speed,high_max_speed)*5)/18
    # interior_speed = (random.randint(int_min_speed,int_max_speed)*5)/18
    highway_speed = (60*5)/18
    interior_speed = (40*5)/18
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


def findOptimalCS(pastData,weightage,reqTime,reqX,reqY, soc, batteryCapacityUser, ecrUser):
    A = [reqX,reqY]
    
    tmp = sys.maxsize
    
    ans = []
    for i in range(numberOfChargingStations):
        B = [CSx[i],CSy[i]]
        c = distanceBetweenAB(A,B)
        
        d = computeSOC(soc,batteryCapacityUser,ecrUser)
        # print(d)
        if c < d:
            tt = timeToTravel(A,B)
            wt = waitingTime(reqTime + tt,occupancyTime[i],pastData[i],weightage)
            if tt + wt  < tmp:
                ans = [i,tt,wt]
                tmp = tt+wt
    return ans

totalTime=[]
waitTime = []
distanceWise = []
distanceCSToDest = []
def solveRequests(pastData,noOfRequests,weightage):
 
    
    global totalTime
    global waitTime
    global distanceWise
    global distanceCSToDest

    for i in range(noOfRequests):
        optimalCS = findOptimalCS(pastData,weightage,randomTime[i],randomX[i],randomY[i], soc[i], batteryCapacityUser[i], ecrUser[i])
        ind = optimalCS[0]
        tt =  optimalCS[1]
        wt = optimalCS[2]
        
        # if(i == 0 and randomTime[i] == 11 and randomX[i] == 7667 and randomY[i] == 3901):
        #     print("tt",tt)
        #     print("wt",wt)
        #     print("ttToDest",ttToDest)
        #     print("distBD",distBD)
        
        
        
        X = [randomX[i],randomY[i]]
        Y = [CSx[ind],CSy[ind]]
        Z = [destX[i],destY[i]]
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

df669 = pd.DataFrame({'ChargingStationCode':ChargingStationCode})
df669.to_csv('datasetWithOnlySOCOptimization.csv',index=False)
df669=pd.read_csv('datasetWithOnlySOCOptimization.csv')

def generateHourlyData(day):

    if day==0:
        for i in range(24):
            requests = vehicleDensity(i)
            generateRequest(startTime + (i*3600),GridX,GridY,requests)
            pastData = [0] * 25
            solveRequests(pastData,requests,day/10)
            z='AverageTime'+str(i)+"(seconds)"
            df669.insert(i+1,z,averageActulTime)
            makeZero(averageActulTime)
            makeZero(noOfCars)
            restart()

    else:
        if day >= 7:
            day = 7
        elif day >= 20:
            day = 8
        for i in range(24):
            requests = vehicleDensity(i)
            z='AverageTime'+str(i)+"(seconds)"
            pastData = df669[z].tolist()
            generateRequest(startTime + (i*3600),GridX,GridY,requests)
            solveRequests(pastData,requests,day/10)
            df669[z] = averageActulTime
            makeZero(averageActulTime)
            makeZero(noOfCars)
            restart()
    makeZero(occupancyTime)
    df669.to_csv('datasetWithOnlySOCOptimization.csv',index=False)

for i in range(10):
    print(i)
    generateHourlyData(i)

def initiliaze(requests):
    for i in range(requests):
        semifinalans.append(0)
        allocatedCS.append(0)
        arrivalTime.append(0)

df669=pd.read_csv('datasetWithOnlySOCOptimization.csv')
df19 = pd.read_csv('newrandomdata.csv')
for x in range(24):
    requests = vehicleDensity(x)
    initiliaze(requests)
    totalTime = []
    # distanceCSToDest = []
    waitTime =[]
    distanceWise=[]
    z='AverageTime'+str(x)+"(seconds)"
    pastData = df669[z].tolist()
    m = 'randomTime'+str(x)+'(seconds)'
    n = 'randomX'+str(x)+'(meters)'
    o = 'randomY'+str(x)+'(meters)'
    p = 'soc'+str(x)
    q = 'batteryCapacityUser'+str(x)+'(kwh)'
    r = 'ecrUser'+str(x)+'(kwh/km)'
    s = 'destX'+str(x)+'(meters)'
    t = 'destY'+str(x)+'(meters)'
    randomTime = df19[m].tolist()[:requests]
    randomX = df19[n].tolist()[:requests]
    randomY = df19[o].tolist()[:requests]
    soc = df19[p].tolist()[:requests]
    batteryCapacityUser = df19[q].tolist()[:requests]
    ecrUser = df19[r].tolist()[:requests]
    destX = df19[s].tolist()[:requests]
    destY = df19[t].tolist()[:requests]
    # print("hhi",randomY)
    solveRequests(pastData,requests,0.7)
    # print(len(sams), requests)
    final_ans_waitTime.append(waitTime)
    final_ans_distance.append(distanceWise)
    # final_ans_distanceCSToDest.append(distanceCSToDest)
    final_ans.append(totalTime)
    # print(distanceWise)
    # print(totalTime)
    # print("xxd")
    # print(waitTime)
    semifinalans = []
    allocatedCS = []
    arrivalTime = []

    
    makeZero(averageActulTime)
    makeZero(noOfCars)
    restart()

df83 = pd.DataFrame({'withSOCOnlyOptimizedWaitTime':final_ans_waitTime})
df83.to_csv('withSOCOnlyOptimizedWaitTime.csv',index=False)
df27 = pd.DataFrame({'withSOCOnlyOptimizedTotalTime':final_ans})
df27.to_csv('withSOCOnlyOptimizedTotalTime.csv',index=False)
# pprint("hhi",randomY)rint(randomY)
# print("hhi")
# print(randomY)
df25 = pd.DataFrame({'withSOCOnlyOptimizedDist':final_ans_distance})
df25.to_csv('withSOCOnlyOptimizedDist.csv',index=False)

# df199 = pd.DataFrame({'withOptimizedTime':final_ans_waitTime})
# df199.to_csv('withOptimizedTime.csv',index=False)
# xxxx = final_ans[10]

df113 = pd.DataFrame(list(zip(randomTime,randomX,randomY,soc,destX,destY,batteryCapacityUser,ecrUser,allocatedCS,arrivalTime)),columns=['randomTime','randomX','randomY','soc','destX','destY','batteryCapacityUser','ecrUser','allocatedCS','arrivalTime'])
df113.to_csv('randomTime.csv',index=False)