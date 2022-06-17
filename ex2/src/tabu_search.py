import sys
import os
import time
import copy
import random
import math
import matplotlib.pyplot as plt

from src.graph_data_structs import *
from src.parse_input_file import parse_input_file
from src.hierholzer import euler_tour
from src.metasearch_common_procedures import * 
from src.metasearch_init_procedure import generalInitialization

def tabu_search_algorithm(graph, inits, sols, maxTime=5, maxIter=100, traceMode=False, startTime=-1, debug=False):
    (directedEdges, costDict, pathDict, verticesD, avgPerViolation) = inits
    (solL, solD) = sols
    
    
    bestSolCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
    if debug == True:
        print(bestSolCost)
        initialcost = bestSolCost[0][3]
        print('Initial cost is: ' + str(bestSolCost[0][3]))

    if startTime == -1:
        startTime = time.time()

    c = 0