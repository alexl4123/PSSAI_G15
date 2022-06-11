import random 

from src.graph_data_structs import *
from src.parse_input_file import parse_input_file

from src.metasearch_init_procedure import *
from src.metasearch_common_procedures import *
from src.hill_climbing import * 
from src.evolutionary_algorithm import evolutionaryAlgorithm

def evolutionary_algorithm(graph, inits, maxTime = 6, traceMode = False, verbose = True):
    (directedEdges, costDict, pathDict, verticesD, avgPerViolation) = inits
    trace = []

    result = evolutionaryAlgorithm(inits, graph, maxIter = 100000, populationSize = 4, maxTime = maxTime, traceMode = traceMode, verbose = verbose)

    if traceMode:
        (curBestSol, solutions, trace) = result
    else:
        (curBestSol, solutions) = result


    if traceMode:
        write_trace_to_file(trace, '_evolutionary')


    curBestEvaluation = completeCost(curBestSol[1], curBestSol[0], graph[0], directedEdges, costDict, pathDict, approximate = False)
    if verbose:
        print('Best found tour has cost: ' + str(curBestEvaluation[0][3]))
    tour = repair(curBestSol[1], curBestSol[0], curBestEvaluation, inits, graph, verbose = True)
    write_tour_to_file(tour, '_evolutionary_0')


    for i in range(0, len(solutions)):
        sol = solutions[i]
        trueCost = completeCost(sol[1], sol[0], graph[0], directedEdges, costDict, pathDict, approximate = True)

        tour = repair(sol[1], sol[0], trueCost, inits, graph)

        write_tour_to_file(tour, '_evolutionary_' + str(i+1))


def start_evolutionary_algorithm():
    # Parse input file (file from args) - only needs to be done once
    graph = parse_input_file()
    inits = generalInitialization(graph)
    evolutionary_algorithm(graph, inits)



