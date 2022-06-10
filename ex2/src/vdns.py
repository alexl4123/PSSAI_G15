import sys
import os
import time
import copy
import random

from src.graph_data_structs import *
from src.parse_input_file import parse_input_file
from src.hierholzer import euler_tour

from src.metasearch_common_procedures import * 
from src.metasearch_init_procedure import generalInitialization

# ------------------------------------------------------------------------------------
# - Setup                                                                            -
# ------------------------------------------------------------------------------------

def toBinary(value, numbers):
    arr = []
    for i in range(0, numbers):
        arr.append(0)
    
    v = value
    for i in range(0, numbers):
        if v % 2 == 1:
            arr[i] = 1

        v = int(v / 2)

    return arr

def vdns(graph,
        inits,
        sols,
        maxIter = 1000,
        fullFlag = False,
        startTime = -1,
        maxTime = 60,
        approximateCostCalculation = True,
        traceMode = False,
        debug = False):
    (directedEdges, costDict, pathDict, verticesD, avgPerViolation) = inits
    (solL, solD) = sols

    # ------------------------------------------------------------------------------------
    # - Search Algorithm                                                                 -
    # ------------------------------------------------------------------------------------

    curBestSolCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
    if debug == True:
        print(bestSolCost)
        print('Initial cost is: ' + str(bestSolCost[0][3]))

    if traceMode == True:
        trace = [bestSolCost]

    

    c = 0
    converged = False
    maxVariableDepth = min(len(solL),5)
    
    if startTime == -1:
        startTime = time.time()

    while (c < maxIter and not converged and isInTime(startTime, maxTime)):
       
        converged = True

        for variableDepth in range(0, maxVariableDepth):
            if not isInTime(startTime, maxTime):
                break
            for solIndex in range(0, len(solL) + 1 - variableDepth):
                if not isInTime(startTime, maxTime):
                    break
     
                # Generate all 2^variableDepth possible neighbors
                for j in range(0, 2^variableDepth):
                    if not isInTime(startTime, maxTime):
                        break
     
                    (newSolL, newSolD) = cloneSolutions(solL)
                    changes = []
                    binary = toBinary(j, variableDepth)

                    for k in range(0, len(binary)):
                        if binary[k] == 0:
                            curSol = newSolL[solIndex + k][2]
                            if curSol.getX() == 0:
                                next
                            else:
                                curSol.decX()
                                changes.append((newSolL[solIndex + k][0], newSolL[solIndex + k][1], -1))

                        else:
                            curSol = newSolL[solIndex + k][2]
                            curSol.incX()
                            changes.append((newSolL[solIndex + k][0], newSolL[solIndex + k][1], 1))


                    curCost = iterativeCost(newSolD, newSolL, verticesD, curBestSolCost, changes, avgPerViolation)
                    if curCost[0][3] < curBestSolCost[0][3]:
                        # Sanity check:
                        trueCurCost = completeCost(newSolD, newSolL, graph[0], directedEdges, costDict, pathDict)
                        if trueCurCost[0][3] < curBestSolCost[0][3]:
                            print("<FOUND BETTER SOLUTION WITH COST " + str(trueCurCost[0][3]) + " AND DEPTH " + str(variableDepth) + " (CURRENT: " + str(curBestSolCost[0][3]) + ")>")
                            curBestSolCost = trueCurCost
                            solL = newSolL
                            solD = newSolD
                            converged = False

                    # END THE for j LOOP
                    if not converged:
                        break
                # END THE for solIndex LOOP
                if not converged:
                    break
            # END THE variableDepth LOOP
            if not converged:
                break


    return (solD, solL, curBestSolCost)
 

