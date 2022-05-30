# coding=utf-8
import sys
import os
import time
import copy
import random

# Other graph library - for shortest paths
import networkx as nx
import matplotlib.pyplot as plt

from graph_data_structs import *
from parse_input_file import parse_input_file
from hierholzer import euler_tour

from metasearch_common_procedures import * 

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
    bestSolCost = None
    solL = None
    solD = None

    for i in range(0,100):
        print('Init: ' + str(i))
        (cSolL, cSolD) = initSolutions(directedEdges)

        randomizedInit(cSolL)

        curCost = completeCost(cSolD, cSolL, graph[0], directedEdges, costDict, pathDict)

        violations = violations + curCost[3]
        if violations != 0:
            avgPerViolation = avgPerViolation + ((curCost[0][2] - avgPerViolation) / violations)

        if bestSolCost is None:
            bestSolCost = curCost
            solL = cSolL
            solD = cSolD
        elif curCost[0][3] < bestSolCost[0][3]:
            bestSolCost = curCost
            solL = cSolL
            solD = cSolD

    print('Violations: ' + str(violations) + '::' + str(avgPerViolation))

    return (directedEdges, costDict, pathDict, solL, solD, verticesD, avgPerViolation)


