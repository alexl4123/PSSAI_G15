# coding=utf-8
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

def hillClimber(graph,
        inits,
        sols,
        maxIter = 1000,
        fullFlag = False,
        approximateCostCalculation = True,
        traceMode = False,
        debug = False):
    (directedEdges, costDict, pathDict, verticesD, avgPerViolation) = inits
    (solL, solD) = sols

    # ------------------------------------------------------------------------------------
    # - Search Algorithm                                                                 -
    # ------------------------------------------------------------------------------------

    bestSolCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
    if debug == True:
        print(bestSolCost)
        print('Initial cost is: ' + str(bestSolCost[0][3]))

    if traceMode == True:
        trace = [bestSolCost]

    c = 0
    converged = False
    while (c < maxIter and not converged ):
       
        index = (0, 'cur')
        curBestSolCost = bestSolCost


        i = 0
        converged = True

        for sol in solL:
            sol[2].incX()
            
            if approximateCostCalculation:
                curCost = iterativeCost(solD, solL, verticesD, curBestSolCost, [(sol[0], sol[1], 1)], avgPerViolation)
            else:
                curCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)

            if (curBestSolCost is None or curCost[0][3] < curBestSolCost[0][3]):
                curBestSolCost = curCost
                index = (i, 'incX')

                if traceMode == True:
                    tmpCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
                    trace.append(tmpCost)
            
            # ---------------------------------------------------------------------
            # If better then accept
            if fullFlag == False:
                if curBestSolCost[0][3] < bestSolCost[0][3]:
                    bestSolCost = curBestSolCost
                    converged = False
                    break
            # ---------------------------------------------------------------------

            #print('(' + str(index[0]) + ',' + str(index[1]) + ',' + str(curCost[0]) + ')')

            sol[2].decX()
            if (sol[2].getX() > 0):
                sol[2].decX()

                if approximateCostCalculation:
                    curCost = iterativeCost(solD, solL, verticesD, curBestSolCost, [(sol[0], sol[1], -1)], avgPerViolation)
                else:
                    curCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)

                if (curCost[0][3] < curBestSolCost[0][3]):
                    curBestSolCost = curCost
                    index = (i, 'decX')

                    if traceMode == True:
                        tmpCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
                        trace.append(tmpCost)
                
                # ---------------------------------------------------------------------
                # If better then accept
                if fullFlag == False:
                    if curBestSolCost[0][3] < bestSolCost[0][3]:
                        bestSolCost = curBestSolCost
                        converged = False
                        break
                # ---------------------------------------------------------------------

                #print('(' + str(index[0]) + ',' + str(index[1]) + ',' + str(curCost[0]) + ')')

                sol[2].incX()

            i = i + 1

        if fullFlag == True:   
            if curBestSolCost[0][3] < bestSolCost[0][3]:
                bestSolCost = curBestSolCost
                if index[1] == 'incX':
                    solL[index[0]][2].incX()
                else:
                    solL[index[0]][2].decX()
                print(completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict))
            elif curBestSolCost[0][3] >= bestSolCost[0][3]:
                converged = True

        
        if debug == True:
            print('(' + str(c) + ', best : ' + str(bestSolCost[0]) + ', curBest : ' + str(curBestSolCost[0]) + ')')

        c = c + 1

    bestSolCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
    (solL, solD) = cloneSolutions(solL)
    return (solD, solL, bestSolCost)










