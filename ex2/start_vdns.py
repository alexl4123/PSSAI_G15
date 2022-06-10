from src.graph_data_structs import *
from src.parse_input_file import parse_input_file

from src.metasearch_init_procedure import *
from src.metasearch_common_procedures import *
from src.hill_climbing import * 
import src.vdns as vd

def vdns(graph, inits, maxTime = 60, traceMode = False, verbose = True):
    (directedEdges, costDict, pathDict, verticesD, avgPerViolation) = inits


    #(solL, solD) = initGreedySolutions(inits, graph)

    curBestSol = None
    curBestCost = ((0,0,0,-1),1)

    bestTrace = []

    startTime = time.time()

    for i in range(0, 10000):
        if not isInTime(startTime,maxTime):
            break
        if (i == 0 and graph[2] is not None):
            sol = loadAndParseSolution(graph[2], directedEdges)
            (solL, solD) = sol
        else:
            (solL, solD) = initSolutions(inits[0])
            randomizedInit(solL)
            #(solL, solD) = initGreedySolutions(inits, graph)

        cost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
         
        result = vd.vdns(graph, inits, (solL, solD), startTime = startTime, maxTime = maxTime, traceMode = traceMode, verbose = verbose)
        if traceMode:
            (solD, solL, bestSolCost, trace) = result
        else:
            (solD, solL, bestSolCost) = result

        cost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)

        if curBestCost[0][3] == -1 or cost[0][3] < curBestCost[0][3]:
            curBestCost = cost
            curBestSol = (solD, solL, bestSolCost)
            bestTrace = trace
            if verbose:
                print("<Accepted with: " + str(curBestCost[0][3]) + ">")
         
    
    if verbose:
        print("<<<BEST SOL WITH COST: " + str(curBestCost[0][3]) + ">>>")

    cost = completeCost(curBestSol[0], curBestSol[1], graph[0], directedEdges, costDict, pathDict)
    tour = repair(curBestSol[0], curBestSol[1], cost, inits, graph, verbose = True)
    write_tour_to_file(tour, '_vdns')

    if traceMode:
        write_trace_to_file(bestTrace, '_vdns')

def start_vdns():
    # Parse input file (file from args) - only needs to be done once
    graph = parse_input_file()
    inits = generalInitialization(graph)
    vdns(graph, inits)


