import random
from copy import deepcopy as cp

def fitToProb(p):
    sum = 0
    for x in range(8):
        for y in range(8):
           sum += p[x][y]
    for x in range(8):
        for y in range(8):
            p[x][y] /= sum

def pickByProb(p):
    while True:
        sum = 0
        pick = random.random()
        for x in range(8):
            for y in range(8):
                sum += p[x][y]
                if pick < sum:
                    return x, y

def pickByMax(p):
    res = 0, 0
    maxValue = float('-inf')
    for x in range(8):
        for y in range(8):
            if maxValue < p[x][y]:
                maxValue = p[x][y]
                res = x, y
    return res

def flat(p):
    res = []
    for x in range(8):
        for y in range(8):
            res.append(p[x][y])
    return res

def rotate(p, r):
    res = [[None for y in range(8)] for x in range(8)]
    if r == 0:
        for x in range(8):
            for y in range(8):
                res[x][y] = p[x][y]
    elif r == 1:
        for x in range(8):
            for y in range(8):
                res[x][y] = p[7-y][x]
    elif r == 2:
        for x in range(8):
            for y in range(8):
                res[x][y] = p[7-x][7-y]
    elif r == 3:
        for x in range(8):
            for y in range(8):
                res[x][y] = p[y][7-x]
    elif r == 4:
        for x in range(8):
            for y in range(8):
                res[x][y] = p[y][x]
    elif r == 5:
        for x in range(8):
            for y in range(8):
                res[x][y] = p[x][7-y]
    elif r == 6:
        for x in range(8):
            for y in range(8):
                res[x][y] = p[7-y][7-x]
    elif r == 7:
        for x in range(8):
            for y in range(8):
                res[x][y] = p[7-x][y]
    return res


