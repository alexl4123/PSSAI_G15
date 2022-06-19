from src.graph_data_structs import *
from src.parse_input_file import parse_input_file
from src.metasearch_init_procedure import *
from src.metasearch_common_procedures import *
from src.load_solution import loadAndParseSolution
from src.simmulated_annealing import simmulated_annealing_algorithm

def simmulated_annealing(graph, inits, maxTime, traceMode=False, verbose=True):
    (directedEdges, costDict, pathDict, verticesD, avgPerViolation) = inits

    if (graph[2] is not None): # given tourPath (e.g. from win's algorithm)
        sol = loadAndParseSolution(graph[2], directedEdges)
        (solL, solD) = sol
    else:
        #(solL, solD) = initSolutions(inits[0])
        #randomizedInit(solL)
        (solL, solD) = initGreedySolutions(inits, graph)

    initC = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)

    result = simmulated_annealing_algorithm(graph, inits, (solL, solD), maxTime=maxTime, traceMode=traceMode)
    
    if traceMode:
        (solD, solL, bestSolCost, trace) = result
    else: 
        (solD, solL, bestSolCost) = result        
    

    cost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
    if verbose:
        print("Init cost: ", initC)
        print("After algo cost: ", cost)
    
    tour = repair(solD, solL, cost, inits, graph, verbose = True)
    write_tour_to_file(graph, tour, '_simmulated_annealing')

    if traceMode:
        write_trace_to_file(graph, trace, '_simmulated_annealing')