from src.graph_data_structs import *
from src.parse_input_file import parse_input_file

from src.metasearch_init_procedure import generalInitialization, initSolutions, randomizedInit
from src.metasearch_common_procedures import *
from src.hill_climbing import * 

def randomized_hill_climber(graph, inits, maxTime = 60, traceMode = False, verbose = True):
    (directedEdges, costDict, pathDict, verticesD, avgPerViolation) = inits
    curBest = -1
    bestSolL = []
    bestSolD = {}

    if verbose:
        print("<<<<<<<<<<<<<<<")
    maxIter = 10000
    trace = []

    startTime = time.time()

    for i in range(0, maxIter):
        if not isInTime(startTime, maxTime):
            break
        if verbose:
            print("Iter " + str(i) + " of " + str(maxIter))

        if (i == 0 and graph[2] is not None):
            # One can specify a tour as a possible 'best' tour
            sol = loadAndParseSolution(graph[2], directedEdges)
            (solL, solD) = sol
        else:
            (solL, solD) = initSolutions(inits[0])
            randomizedInit(solL)

        (solD, solL, bestSolCost) = hillClimber(graph, inits, (solL, solD), startTime = startTime, maxTime = maxTime)
        if verbose: 
            print(">> GOT: " + str(bestSolCost[0][3]) + ", CUR BEST: " + str(curBest) + "<<")

        if (bestSolCost[0][3] < curBest) or curBest == -1:
            curBest = bestSolCost[0][3]
            bestSolL = solL
            bestSolD = solD
            if traceMode:
                trace.append(bestSolCost)
    if verbose:
        print("<<<<<<<<<<<<<<<")

    cost = completeCost(bestSolD, bestSolL, graph[0], directedEdges, costDict, pathDict, approximate = False)
    tour = repair(bestSolD, bestSolL, bestSolCost, inits, graph, verbose = True)
    write_tour_to_file(tour, '_randomized_hill_climber')

    if traceMode:
        write_trace_to_file(trace, '_randomized_hill_climber')



def start_random_hill_climber():
    # Parse input file (file from args) - only needs to be done once
    graph = parse_input_file()
    inits = generalInitialization(graph)
    randomized_hill_climber(graph, inits)
