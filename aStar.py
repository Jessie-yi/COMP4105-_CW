# aStar.py
# Description:
# A* pathfinding algorithm used for grid-based robot navigation.

# This file is based on the version provided in the COMP4030 course materials (aStar.py).
# Minor adjustments were made to variable naming and formatting for improved readability and integration.

import numpy as np
import random

def makeSpecificGrid():
    grid = np.zeros((10,10),dtype=np.int16)
    for xx in range(10):
        for yy in range(10):
                grid[xx][yy] = random.randrange(1,3)
    grid[8][9] = 5
    for yy in range(0,9):
        grid[8][yy] = random.randrange(4,5)
    for xx in range(1,8):
        grid[xx][0] = random.randrange(4,5)
    grid[0][0] = 1
    grid[9][9] = 0
    print(grid)
    return grid

def makeSpecificGrid2():
    grid = np.zeros((10,10),dtype=np.int16)
    for xx in range(10):
        for yy in range(10):
                grid[xx][yy] = random.randrange(1,3)
    for xx in range(0,9):
        grid[xx][xx] = random.randrange(4,5)
    grid[0][0] = 1
    grid[9][9] = 0
    print(grid)
    return grid


def aStarSearch(grid):
    heuristicGrid = np.zeros((10,10),dtype=np.int16)
    for xx in range(10):
        for yy in range(10):
            heuristicGrid[xx][yy] = 10*(xx + yy)
    #print(heuristicGrid)
    bestForPosition = np.zeros((10,10),dtype=np.int16)
    #visitedList = {}
    #visitedList[(9,9)] = heuristicGrid[9,9]
    currentlyActiveList = []
    currentPosition = (9,9)
    currentlyActiveList.append( (currentPosition,heuristicGrid[9][9]) ) # coordinates, a* value

    ## Build bestForPosition table
    while currentlyActiveList:
        currentlyActiveList = [item for item in currentlyActiveList if item[0] != currentPosition]

        if currentPosition[0]>0:
            x1, y1 = currentPosition[0] - 1, currentPosition[1]
            aStarScore1 = bestForPosition[currentPosition[0]][currentPosition[1]] \
                          + grid[x1][y1] + heuristicGrid[x1][y1]
            currentlyActiveList.append(((x1, y1), aStarScore1))
            bestForPosition[x1][y1] = max(
                bestForPosition[currentPosition[0]][currentPosition[1]] + grid[x1][y1],
                bestForPosition[x1][y1])

        if currentPosition[1]>0:
            x2, y2 = currentPosition[0], currentPosition[1] - 1
            aStarScore2 = bestForPosition[currentPosition[0]][currentPosition[1]] \
                          + grid[x2][y2] + heuristicGrid[x2][y2]
            currentlyActiveList.append(((x2, y2), aStarScore2))
            bestForPosition[x2][y2] = max(
                bestForPosition[currentPosition[0]][currentPosition[1]] + grid[x2][y2],
                bestForPosition[x2][y2])

        currentlyActiveList.sort(key=lambda t: t[1], reverse=True)
        #print("currently active: ",currentlyActiveList)
        if not currentlyActiveList:
            break
        currentPosition = currentlyActiveList[0][0]
        #print(currentPosition)
        #print(grid)
        #print(bestForPosition)
        #input()
    ## construct best path
    #print(bestForPosition)
    pathGrid = np.zeros( (10,10), dtype=np.int8) #just for illustration
    path = []
    currentPosition = (9,9)
    path.append( (9,9) )
    pathGrid[9][9] = True

    MAX_PATH_STEPS = 200
    step_count = 0

    while currentPosition != (0,0):
        step_count += 1
        if step_count > MAX_PATH_STEPS:
            print("[ERROR] A* exceeded max path steps. Returning empty path.")
            return []

        pos1 = pos2 = False
        if currentPosition[0]>0:
            possPosition1x = currentPosition[0]-1
            possPosition1y = currentPosition[1]
            pos1 = True
        if currentPosition[1]>0:
            possPosition2x = currentPosition[0]
            possPosition2y = currentPosition[1]-1
            pos2 = True

        pos1Bigger = False
        if pos1 and pos2:
            pos1Bigger = bestForPosition[possPosition1x][possPosition1y] > bestForPosition[possPosition2x][possPosition2y]

        if (pos1 and not pos2) or (pos1 and pos2 and pos1Bigger):
            path.append( (possPosition1x,possPosition1y) )
            pathGrid[possPosition1x][possPosition1y] = 1
            currentPosition = (possPosition1x,possPosition1y)
        elif (pos2 and not pos1) or (pos1 and pos2 and not pos1Bigger):
            path.append( (possPosition2x,possPosition2y) )
            pathGrid[possPosition2x][possPosition2y] = 1
            currentPosition = (possPosition2x,possPosition2y)
        else:
            print("[ERROR] No valid next step. Returning empty path.")
            return[]
    #print(grid)
    #print(path)
    #print(pathGrid)
    # Ensure path is returned if constructed successfully
    return(path)

#aStarSearch(makeSpecificGrid())
#aStarSearch(makeSpecificGrid2())

    
