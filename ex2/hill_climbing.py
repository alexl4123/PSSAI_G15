# coding=utf-8
import sys
import os
import time
import copy
import random

from ortools.graph import pywrapgraph
from ortools.sat.python import cp_model
from ortools.linear_solver import pywraplp

import multiprocessing

# Other graph library - for shortest paths
import networkx as nx
import matplotlib.pyplot as plt

from graph_data_structs import *
from parse_input_file import parse_input_file
from hierholzer import euler_tour

# ------------------------------------------------------------------------------------
# - Some Helper Functions                                                            -
# ------------------------------------------------------------------------------------

def validInit(solL):
    for sol in solL:
        sol[2].incX()

def randomizedInit(solL):
    for sol in solL:
        randNum = random.randint(0,1)
        if randNum == 1:
            sol[2].incX()

def validWpp(vertices, edges, solD):

    for edge in edges:
        s = solD[str(edge.i) + ':' + str(edge.j)].getX() + solD[str(edge.j) + ':' + str(edge.i)].getX()
        if (s != 2):
            print('<<Constraint Violation found for: (' + str(edge.i) + str(edge.j) + ')')

    for vertex in vertices:
        s = 0
        for edge in vertex.getEdges():
            if vertex.name == edge.i:
                s = s + solD[str(edge.i) + ':' + str(edge.j)].getX()
            else:
                s = s - solD[str(edge.i) + ':' + str(edge.j)].getX()

        if (s != 0):
            print('<#<Constraint Violation found for vertex: (' + str(vertex.name) +  ')')

def completeCost(solD, solL, vertices, edges, costDict, pathDict):
    totalCost = 0
   
    # Basic Costs
    for sol in solL:
        totalCost = totalCost + sol[2].cost()

    # CS2 Costs
    cs2Errors = []

    for edge in edges:
        s = solD[str(edge.i) + ':' + str(edge.j)].getX() + solD[str(edge.j) + ':' + str(edge.i)].getX()
        if s == 0:
            totalCost = totalCost + solD[str(edge.i) + ':' + str(edge.j)].singleCost() + solD[str(edge.j) + ':' + str(edge.i)].singleCost()
            cs2Errors.append((str(edge.i), str(edge.j)))
            cs2Errors.append((str(edge.j), str(edge.i)))
    
    # -------------------------------------------------------------------------------
    # CS3 Costs
    cs3Errors = []
    eNegCs3Errors = []
    ePosCs3Errors = []

    cs3VerticesAmount = 0

    usedVertices = {}

    for vertex in vertices:
        s = 0
        for edge in vertex.getEdges():
            if str(vertex.name) == str(edge.i):
                s = s + solD[str(edge.i) + ':' + str(edge.j)].getX()
                s = s - solD[str(edge.j) + ':' + str(edge.i)].getX()
            else:
                s = s + solD[str(edge.j) + ':' + str(edge.i)].getX()
                s = s - solD[str(edge.i) + ':' + str(edge.j)].getX()
        
        if s < 0:
            for i in range(0,abs(s)):
                eNegCs3Errors.append((vertex.name, cs3VerticesAmount))
                usedVertices[cs3VerticesAmount] = vertex.name
                cs3VerticesAmount = cs3VerticesAmount + 1
        elif s > 0:
            for i in range(0,abs(s)):
                ePosCs3Errors.append((vertex.name, cs3VerticesAmount))
                usedVertices[cs3VerticesAmount] = vertex.name
                cs3VerticesAmount = cs3VerticesAmount + 1

    if len(eNegCs3Errors) > 0 or len(ePosCs3Errors) > 0:
        # If Constraint 3 is violated, compute perfect matching between those violations in terms of minimum repair cost

        mcpm = []

        for neg in eNegCs3Errors:
            for pos in ePosCs3Errors:
                mcpm.append((int(neg[1]), int(pos[1]), costDict[str(neg[0]) + ':' + str(pos[0])]))
            
        mcpm_path = '../ex1/mcpm'
        input_file_path = mcpm_path + '/tmp'

        f = open(input_file_path, 'w')
        
        f.write(str(cs3VerticesAmount) + "\n")
        f.write(str(len(mcpm)) + "\n")

        for pair in mcpm:
            f.write(str(pair[0]) + ' ' + str(pair[1]) + ' ' + str(pair[2]) + '\n')

        f.close()   
        
        # Invoke polynomial solver of minimum-cost-perfect-matching
        stream = os.popen(mcpm_path + '/example -f ' + input_file_path + ' --minweight')
        output = stream.read()

        lines = output.splitlines()
        for index in range(len(lines)):
            if index == 0:
                line = lines[index]
                splits = line.split(' ')
                totalCost = totalCost + (int(splits[len(splits) - 1]))
            elif index == 1:
                pass
            else:
                line = lines[index]
                splits = line.split(' ')

                cs3Errors.append((usedVertices[int(splits[0])], usedVertices[int(splits[1])]))

    return (totalCost, cs2Errors, cs3Errors)

# ------------------------------------------------------------------------------------
# - Setup                                                                            -
# ------------------------------------------------------------------------------------

# Parse input file (file from args)
graph = parse_input_file()

fullFlag = False
if len(sys.argv) == 3:
    flag = sys.argv[2]
    if flag == 'full':
        fullFlag = True
    elif flag == 'part':
        fullFlag = False
    else:
        print("Error: synopsis is: program file [full|part]")
        quit()

directedEdges = []
for edge in graph[1]:
    directedEdges.append(DirectedEdge(edge.i, edge.j, edge.ij))
    directedEdges.append(DirectedEdge(edge.j, edge.i, edge.ji))

G = nx.DiGraph()

for edge in directedEdges:
    G.add_edge(int(edge.i), int(edge.j), weight=edge.cost)

nx.draw(G, with_labels=True, font_weight='bold')
plt.savefig('toy-directed.png')

p = dict(nx.all_pairs_dijkstra(G))

costDict = {}
pathDict = {}
for v1 in graph[0]:
    for v2 in graph[0]: 
        costDict[str(v1.name) + ':' +str(v2.name)] = p[int(v1.name)][0][int(v2.name)]
        pathDict[str(v1.name) + ':' +str(v2.name)] = p[int(v1.name)][1][int(v2.name)]

        costDict[str(v2.name) + ':' +str(v1.name)] = p[int(v2.name)][0][int(v1.name)]
        pathDict[str(v2.name) + ':' +str(v1.name)] = p[int(v2.name)][1][int(v1.name)]

solL = []
solD = {}

for edge in directedEdges:
    curSol = SolutionRepresentation(edge.cost)
    solL.append((edge.i,edge.j,curSol))
    solD[str(edge.i) + ':' +str(edge.j)] = curSol



# ------------------------------------------------------------------------------------
# - Initialize                                                                       -
# ------------------------------------------------------------------------------------

# Setting all x_{i,j} to 1 is a valid solution

# toy2 - CS3 test example
"""
solD[str(1) + ':' +str(2)].incX()
solD[str(2) + ':' +str(3)].incX()
solD[str(3) + ':' +str(4)].incX()
solD[str(2) + ':' +str(4)].incX()
solD[str(4) + ':' +str(1)].incX()
solD[str(1) + ':' +str(4)].incX()
"""

# validInit(solL)
randomizedInit(solL)

# ------------------------------------------------------------------------------------
# - Search Algorithm                                                                 -
# ------------------------------------------------------------------------------------

bestSolCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
print(bestSolCost)
print('Initial cost is: ' + str(bestSolCost[0]))

c = 0
converged = False
while (c < 100 and not converged ):
   
    index = (0, 'cur')
    curBestSolCost = None


    i = 0
    converged = True

    for sol in solL:
        sol[2].incX()

        curCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
        if (curBestSolCost is None or curCost[0] < curBestSolCost[0]):
            curBestSolCost = curCost
            index = (i, 'incX')
        
        
        # ---------------------------------------------------------------------
        # If better then accept
        if fullFlag == False:
            if curBestSolCost[0] < bestSolCost[0]:
                bestSolCost = curBestSolCost
                converged = False
                break
        # ---------------------------------------------------------------------

        #print('(' + str(index[0]) + ',' + str(index[1]) + ',' + str(curCost[0]) + ')')

        sol[2].decX()
        if (sol[2].getX() > 0):
            sol[2].decX()

            curCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
            if (curCost[0] < curBestSolCost[0]):
                curBestSolCost = curCost
                index = (i, 'decX')
        
            # ---------------------------------------------------------------------
            # If better then accept
            if fullFlag == False:
                if curBestSolCost[0] < bestSolCost[0]:
                    bestSolCost = curBestSolCost
                    converged = False
                    break
            # ---------------------------------------------------------------------

            #print('(' + str(index[0]) + ',' + str(index[1]) + ',' + str(curCost[0]) + ')')

            sol[2].incX()

        i = i + 1

    if fullFlag == True:   
        if curBestSolCost[0] < bestSolCost[0]:
            bestSolCost = curBestSolCost
            if index[1] == 'incX':
                print('inc')
                solL[index[0]][2].incX()
            else:
                print('dec')
                solL[index[0]][2].decX()
            print(completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict))
        elif curBestSolCost[0] >= bestSolCost[0]:
            converged = True


    print('(' + str(c) + ', best : ' + str(bestSolCost[0]) + ', curBest : ' + str(curBestSolCost[0]) + ')')
    c = c + 1





# ------------------------------------------------------------------------------------
# - Repair                                                                           -
# ------------------------------------------------------------------------------------

bestSolCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
print(bestSolCost)
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

input_file_path = sys.argv[1]
input_file_name = input_file_path.split('/')

input_file_name = input_file_name[len(input_file_name) - 1]

output_file_path = 'tours/' + input_file_name + '_hill_climbing'

f = open(output_file_path, 'w')

f.write(str(wpp_tour) + '\n')

f.close()










