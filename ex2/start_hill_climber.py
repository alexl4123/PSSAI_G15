from src.graph_data_structs import *
from src.parse_input_file import parse_input_file

from src.metasearch_init_procedure import *
from src.metasearch_common_procedures import *
from src.hill_climbing import * 
from src.load_solution import loadAndParseSolution



def hill_climber(graph, inits, maxTime = 60, traceMode = False, verbose = True): 
    (directedEdges, costDict, pathDict, verticesD, avgPerViolation) = inits
    trace = []

    if (graph[2] is not None):
        sol = loadAndParseSolution(graph[2], directedEdges)
        (solL, solD) = sol
    else:
        #(solL, solD) = initSolutions(inits[0])
        #randomizedInit(solL)
        (solL, solD) = initGreedySolutions(inits, graph)

    cost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
    if verbose:
        print('Cur cost 3: ' + str(cost))

    result = hillClimber(graph, inits, (solL, solD), maxTime = maxTime, traceMode = traceMode)
    if traceMode:
        (solD, solL, bestSolCost, trace) = result
    else: 
        (solD, solL, bestSolCost) = result

    cost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict, approximate = False)
    if verbose:
        print('Cur cost 4: ' + str(cost))
    tour = repair(solD, solL, cost, inits, graph, verbose = True)
    write_tour_to_file(tour, '_hill_climber')

    if traceMode:
        write_trace_to_file(trace, '_hill_climber')

def start_hill_climber():
    # Parse input file (file from args) - only needs to be done once
    graph = parse_input_file()
    inits = generalInitialization(graph)
    hill_climber(graph, inits)
