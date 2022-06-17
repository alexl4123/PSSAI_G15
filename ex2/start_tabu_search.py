from src.graph_data_structs import *
from src.parse_input_file import parse_input_file
from src.metasearch_init_procedure import *
from src.metasearch_common_procedures import *
from src.load_solution import loadAndParseSolution
from src.tabu_search import tabu_search_algorithm

def tabu_search(graph, inits, maxTime = 60, traceMode = False, verbose = True):
    (directedEdges, costDict, pathDict, verticesD, avgPerViolation) = inits


    # consider using wins algorithm instead


    (solL, solD) = initSolutions(inits[0])
    randomizedInit(solL)

    initC = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)

    result = tabu_search_algorithm(graph, inits, (solL, solD), maxTime=maxTime, traceMode=traceMode)
    (solD, solL, bestSolCost) = result

    cost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
    if verbose:
        print("Init cost: ", initC)
        print("After algo cost: ", cost)
    
    tour = repair(solD, solL, cost, inits, graph, verbose = True)
    write_tour_to_file(tour, '_tabu_search')

