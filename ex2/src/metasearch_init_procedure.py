# coding=utf-8
import sys
import os
import time
import copy
import random

# Other graph library - for shortest paths
import networkx as nx
import matplotlib.pyplot as plt

from src.graph_data_structs import *
from src.parse_input_file import parse_input_file
from src.hierholzer import euler_tour

from src.metasearch_common_procedures import * 

def generalInitialization(graph):

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

    verticesD = {}
    for vertice in graph[0]:
        verticesD[str(vertice.name)] = vertice

    # validInit(solL)
    avgPerViolation = 0
    violations = 0

    for i in range(0,100):
        print('Init: ' + str(i))
        (cSolL, cSolD) = initSolutions(directedEdges)

        randomizedInit(cSolL)

        curCost = completeCost(cSolD, cSolL, graph[0], directedEdges, costDict, pathDict)

        violations = violations + curCost[3]
        if violations != 0:
            avgPerViolation = avgPerViolation + ((curCost[0][2] - avgPerViolation) / violations)

    print('Violations: ' + str(violations) + '::' + str(avgPerViolation))

    return (directedEdges, costDict, pathDict, verticesD, avgPerViolation)


def validInit(solL):
    for sol in solL:
        sol[2].incX()

def randomizedInit(solL):
    for sol in solL:
        sol[2].reset()
        randNum = random.randint(0,1)
        if randNum == 1:
            sol[2].incX()

def initSolutions(directedEdges):
    solL = []
    solD = {}

    for edge in directedEdges:
        curSol = SolutionRepresentation(edge.cost)
        solL.append((edge.i,edge.j,curSol))
        solD[str(edge.i) + ':' +str(edge.j)] = curSol
    
    return(solL, solD)

def initGreedySolutions(inits, graph):
    vertices = graph[0]
    (directedEdges, costDict, pathDict, verticesD, avgPerViolation) = inits
    solL = []
    solD = {}

    for edge in directedEdges:
        curSol = SolutionRepresentation(edge.cost)
        solL.append((edge.i,edge.j,curSol))
        solD[str(edge.i) + ':' +str(edge.j)] = curSol

    curV = vertices[0]

    # Step 1 - Create initial solution
    for otherV in vertices:
        if (curV.equals(otherV)):
            next
        
        pathTo = pathDict[(str(curV.name) + ':' + str(otherV.name))]
        pathFrom = pathDict[(str(otherV.name) + ':' + str(curV.name))]

        for index in range(1, len(pathTo)):
            lastPV = pathTo[index-1]
            curPV = pathTo[index]

            curSol = solD[str(lastPV) + ':' + str(curPV)]
            if (curSol.getX() == 0):
                curSol.incX()
    
    # Step 2 - If both directions 0 -> Add lower cost one
    for edgeIndex in range(0, len(directedEdges), 2):
        to = solL[edgeIndex][2]
        fr = solL[edgeIndex + 1][2]

        if (to.getX() == 0 and fr.getX() == 0) and (to.singleCost() < fr.singleCost()):
            to.setX(1)
        elif (to.getX() == 0 and fr.getX() == 0):
            fr.setX(1)

    # Step 3 - Repair
    cost = completeCost(solD, solL, vertices, directedEdges, costDict, pathDict)
    repair(solD, solL, cost, inits, graph)
    
    # Step 4 - Remove simple unnecessary edges
    for edgeIndex in range(0, len(directedEdges), 2):
        to = solL[edgeIndex][2]
        fr = solL[edgeIndex + 1][2]

        min_ = min(to.getX(), fr.getX())

        if (to.getX() == fr.getX()):
            min_ = min_ - 1

        to.setX(to.getX() - min_)
        fr.setX(fr.getX() - min_)

    """
    costDict[str(v1.name) + ':' +str(v2.name)] = p[int(v1.name)][0][int(v2.name)]
    pathDict[str(v1.name) + ':' +str(v2.name)] = p[int(v1.name)][1][int(v2.name)]

    costDict[str(v2.name) + ':' +str(v1.name)] = p[int(v2.name)][0][int(v1.name)]
    pathDict[str(v2.name) + ':' +str(v1.name)] = p[int(v2.name)][1][int(v1.name)]
    """

    
    return(solL, solD)



