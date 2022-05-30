# coding=utf-8
import sys
import os
import time
import copy
import random

from graph_data_structs import *
from parse_input_file import parse_input_file
from hierholzer import euler_tour

from metasearch_common_procedures import * 
from metasearch_init_procedure import generalInitialization

# ------------------------------------------------------------------------------------
# - Setup                                                                            -
# ------------------------------------------------------------------------------------

def hillClimber(graph, inits, fullFlag = False, approximateCostCalculation = True):
    (directedEdges, costDict, pathDict, solL, solD, verticesD, avgPerViolation) = inits

    # ------------------------------------------------------------------------------------
    # - Search Algorithm                                                                 -
    # ------------------------------------------------------------------------------------

    bestSolCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
    print(bestSolCost)
    print('Initial cost is: ' + str(bestSolCost[0][3]))

    c = 0
    converged = False
    while (c < 1000 and not converged ):
       
        index = (0, 'cur')
        curBestSolCost = bestSolCost


        i = 0
        converged = True

        for sol in solL:
            sol[2].incX()
            
            if approximateCostCalculation:
                curCost = iterativeCost(solD, solL, verticesD, curBestSolCost, (sol[0], sol[1], 1), avgPerViolation)
            else:
                curCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)

            if (curBestSolCost is None or curCost[0][3] < curBestSolCost[0][3]):
                curBestSolCost = curCost
                index = (i, 'incX')
            
            
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
                    curCost = iterativeCost(solD, solL, verticesD, curBestSolCost, (sol[0], sol[1], -1), avgPerViolation)
                else:
                    curCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)

                if (curCost[0][3] < curBestSolCost[0][3]):
                    curBestSolCost = curCost
                    index = (i, 'decX')
            
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
                    print('inc')
                    solL[index[0]][2].incX()
                else:
                    print('dec')
                    solL[index[0]][2].decX()
                print(completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict))
            elif curBestSolCost[0][3] >= bestSolCost[0][3]:
                converged = True


        print('(' + str(c) + ', best : ' + str(bestSolCost[0]) + ', curBest : ' + str(curBestSolCost[0]) + ')')
        c = c + 1

    bestSolCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
    (solL, solD) = cloneSolutions(solL)
    return (solD, solL, bestSolCost)


def repair(solD, solL, bestSolCost, inits, graph):
    (directedEdges, costDict, pathDict, oldSolL, oldSolD, verticesD, avgPerViolation) = inits
    
    bestSolCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)

    cs2Repair = bestSolCost[1]

    for cs2 in cs2Repair:
        solD[cs2[0] + ':' + cs2[1]].incX()

    cs3Repair = bestSolCost[2]

    for cs3 in cs3Repair:
        path = pathDict[cs3[0] + ':' + cs3[1]]
        print(path)

        for index in range(0, len(path) - 1):
            solD[str(path[index]) + ':' + str(path[index+1])].incX()

    bestSolCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
    print(bestSolCost)

    solverValuesCopy = []
    for edge in directedEdges:
        for i in range(0, solD[str(edge.i) + ':' + str(edge.j)].getX()):
            solverValuesCopy.append((int(edge.i), int(edge.j)))

    wpp_tour = euler_tour(solverValuesCopy.copy(), solverValuesCopy[0][0])
    print("<<<<<<POSSIBLE_TOUR>>>>>>>>>>>")
    print(wpp_tour)
    print("<<<<<<POSSIBLE_TOUR_END>>>>>>>>>>>")

def write_tour_to_file(wpp_tour):
    input_file_path = sys.argv[1]
    input_file_name = input_file_path.split('/')

    input_file_name = input_file_name[len(input_file_name) - 1]

    output_file_path = 'tours/' + input_file_name + '_hill_climbing'

    f = open(output_file_path, 'w')

    f.write(str(wpp_tour) + '\n')

    f.close()











