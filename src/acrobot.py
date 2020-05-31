#!/usr/bin/env python3

import time
import math
import gym
import sys
import json
from random import choice, random
from loaddb import filldb

mindth1 = 1e9
mindth2 = 1e9
maxdth1 = -1e9
maxdth2 = -1e9

db = {}

wins = 0
loss = 0

env = gym.make('Acrobot-v1')

alpha   = 0.2
eta     = 0.9


def inittable():
     global db

     for m in [-1,1]:           # for action
         for i in range(7):      # for each angle 1
             for j in range(7):     # for each angle 2
                 for k in range(5):    # for each angular velocity 1
                     for l in range(5):    # omega 2
                        db[((i,j,k,l),m)] = 0.5

def getangle(c,s):     # convert sin and cos to angle in degrees
    theta = math.asin(abs(s)) * 180.0 / math.pi
    if s >= 0 and c >= 0:
        answer = theta
    elif s >= 0 and c < 0:
        answer = 180 - theta
    elif s < 0 and c >= 0:
        answer = -theta
    else:
        answer = theta - 180

    return int(answer)  # +180 to -180

# update qtable for given key by reward value

def update(key,reward):
     global db, alpha
     #fd = open("log.txt", "a+")
     #val = db[key]
     #nval = alpha * reward + (1.0 - alpha) * val
     db[key] = alpha * reward + (1.0 - alpha) * db[key]

     #fd.write("Key:{0}, Value:{1}, reward:{2}, update: {3}\n".format(key,val, reward,nval))
     #db[key] = nval
     #fd.close()

def getmove_biased(x):
     global mindth1, mindth2, maxdth1, maxdth2

     theta1 = getangle(x[0],x[1])
     theta2 = getangle(x[2],x[3])
 #   print(theta1,theta2,x[4],x[5])
 #    mindth1 = min(mindth1,x[4])
 #    mindth2 = min(mindth2,x[5])
 #    maxdth1 = max(maxdth1,x[4])
 #    maxdth2 = max(maxdth2,x[5])

     x1 = int(((theta1 + 180) * 7)/360)    # degree
     x2 = int(((theta2 + 180) * 7)/360)
     x3 = int(((x[4] + 12.8) * 5)/25.6)    # angular velocity
     x4 = int(((x[5] + 15.5) * 5)/ 44)
     #print("getting biased moves !!!")
     if x[4] < 0:
         return ((x1,x2,x3,x4),-1)
     return ((x1,x2,x3,x4),1)



def getmove(x):
    global mindth1, mindth2, maxdth1, maxdth2, db, eta

    theta1 = getangle(x[0],x[1])
    theta2 = getangle(x[2],x[3])
#   print(theta1,theta2,x[4],x[5])
#  after 101 games    -11.2532  -10.8535    7.2406   17.3801
#  after 100 games    -12.5664  -15.1388   12.5664   21.1563
#  after 10001 games  -12.5664  -14.9065   12.5664   28.2743

#    mindth1 = min(mindth1,x[4])      #
#    mindth2 = min(mindth2,x[5])      #
#    maxdth1 = max(maxdth1,x[4])      #
#    maxdth2 = max(maxdth2,x[5])      #

    x1 = int(((theta1 + 180) * 7)/360)    # degree
    x2 = int(((theta2 + 180) * 7)/360)
    x3 = int(((x[4] + 12.8) * 5)/25.6)    # angular velocity
    x4 = int(((x[5] + 15.5) * 5)/ 44)
#    x3 = int(((x[4] + 12.8) * 256)/25.6)    # angular velocity
#    x4 = int(((x[5] + 15.5) * 440)/ 44)

    if random() < eta:             # explore or exploit, eta is exploration
        m = choice([-1,1])          # explore
        #print("making Random move !!!")
    else:
        m = max([-1,1], key = lambda k: db[((x1,x2,x3,x4),k)])    # exploit
        #print("Exploit")
    return ((x1,x2,x3,x4),m)

    '''
    #: returning random left / right
    if x[4] < 0:
        return ((x1,x2,x3,x4),-1)
    return ((x1,x2,x3,x4),1)
    '''

def printstuff():
    global db
    #for g in range(7):
    for h in range(7):
             print('move -1, x {0:d} {1:29s} move 1, x {0:d}'.format(h," "))
             for i in range(5):
                for m in [-1,1]:
                    for j in range(5):
                        if ((1,h,i,j),m) in db:
                            print("{0:5.2f}".format(db[((1,h,i,j),m)]), end='')
                        else:
                            print(" -----",end='')
                    if m == -1:
                        print("   |   ", end='')
                print()
    print(len(db), 'database keys')


def writestuff(fd):
    global db
    for g in range(7):
        for h in range(7):
             #print('move -1, x {0:d} {1:29s} move 1, x {0:d}'.format(h," "))
             for i in range(5):
                for m in [-1,1]:
                    for j in range(5):
                        if ((g,h,i,j),m) in db:
                            fd.write("(({0},{1},{2},{3}),{4})={5:5.2f}\n".format(g,h,i,j,m, db[((g,h,i,j),m)] ))
#                            print("{0:5.2f}".format(db[((1,h,i,j),m)]), end='')
#                        else:
#                            print(" -----",end='')
#                    if m == -1:
#                        print("   |   ", end='')
#                print()
#    print(len(db), 'database keys')

def printstuff1():
    global db
    for g in range(15):
         for h in range(15):
             print('move -1, x {0:d} {1:29s} move 1, x {0:d}'.format(h," "))
             for i in range(10):
                for m in [-1,1]:
                    for j in range(10):
                        if ((g,h,i,j),m) in db:
                            print("{0:5.2f}".format(db[((g,h,i,j),m)]), end='')
                        else:
                            print(" -----",end='')
                    if m == 0:
                        print("   |   ", end='')
                print()
    print(len(db), 'database keys')


if __name__ == "__main__":

    argcount = len(sys.argv)
    if argcount  == 1:
        print()
        print("Usage: ./acrobat.py [fast/slow] [Name of file to fill Q-table]")
        print("Game starts with fresh Q-table if no Q-table file is passed")
        print("Program ENDED !!!")
        exit()

    if argcount >= 2:
        qtabFile = 'acrobot.txt'
        if sys.argv[1] == 'fast':
            visual = False
        else:
            visual = True
    if argcount == 3:
        json_writeFile = sys.argv[2]
        filldb(sys.argv[2],db)
        if (len(db) != 2450):
            print("SOME ERROR ")
            exit()


        #with open(json_writeFile, 'r') as fp:
        #    db = json.load(fp)

    else:
        inittable()

    print("Value of visual : ",visual)
    #visual = True
    #inittable()
    total = 0                        # total moves in all games
    allSteps = 0
    a = time.time()
    for games in range(1,100001):
        steps = 0
        x1 = env.reset()
        oldkey = None
        largeOscila = False
        while True:
            steps += 1
            allSteps += 1
            if visual:
                env.render()
            if games % 200 == 0:
                key = getmove_biased(x1)
            else:
                key = getmove(x1)
            x1, x2, done, x3 = env.step(key[1])
#            print(x1,x2,done,x3)
#           print("{0:9.4f} {1:9.4f} {2:9.4f} {3:9.4f}".format(mindth1, mindth2, maxdth1, maxdth2))
       #     if steps % 200 == 0 or done:
            if done and x2 == 0.0:      # if won
                reward = 1.0
            elif done and x2 == -1.0:     # if lost
                reward = 0.0
            else:
                reward = db[key]        # still playing
            if oldkey:
                update(oldkey, reward)
            oldkey = key
            if done:
                eta *= 0.99
                #eta = random()

#               if key[0][2] >= 3 and key[0][3] >= 3:   # for omega div = 10
#                    largeOscila = True
                if x2 == 0.0:
                    #print("Game Won on its own ")
                    wins += 1
                if x2 == -1.0:
                    loss += 1
                print("Games played: ", games, "Steps taken: ", steps)

                if visual or games % 1000 == 0:
                    printstuff()
                    print(steps, 'steps')
                    print("Average steps for last 1000 games",allSteps /1000,'!!!!!!!!!!!!!!!!!!!!!' )
                    print()
                    print(x1, x2, done, x3)
                    allSteps = 0
                  # logging
                    fd = open("log.txt", "a+")
                    fd.write("Last state: {0} wins so far:{1}, lost: {2}, games:{3},eta:{4}\n".format(key,wins, loss, games, eta))
                    fd.close()

                    print("Last state :", key, "wins so far ", wins, "lost: ",loss)

                    b = time.time()
                    print("Time lapsed : ", b -a)
                    #s = input("{0:d} {1:9.6f} ? ".format(games, eta))
                    s = 'v'

                    #if len(s) > 0 and s[0] == 'r':

                    if len(s) > 0  and s[0] == 'v':
                        visual = True
                        print("Writing into File !!!!!")
                        fd = open(qtabFile, "a+")
                        writestuff(fd)
                        fd.close()
                        #with open(json_writeFile, 'w') as fp:
                        #    json.dump(db,fp, indent =4)
                    else:
                        visual = False

                break
    env.close()

