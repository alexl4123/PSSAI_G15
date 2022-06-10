import random 

from src.graph_data_structs import *
from src.parse_input_file import parse_input_file

from src.metasearch_init_procedure import *
from src.metasearch_common_procedures import *
from src.hill_climbing import * 
from src.evolutionary_algorithm import evolutionaryAlgorithm

# Parse input file (file from args)
graph = parse_input_file()

inits = generalInitialization(graph)
(directedEdges, costDict, pathDict, verticesD, avgPerViolation) = inits

(curBestSol, solutions) = evolutionaryAlgorithm(inits, graph, maxIter = 100000, populationSize = 5)

curBestEvaluation = completeCost(curBestSol[1], curBestSol[0], graph[0], directedEdges, costDict, pathDict)
print('Best found tour has cost: ' + str(curBestEvaluation[0][3]))
tour = repair(curBestSol[1], curBestSol[0], curBestEvaluation, inits, graph, verbose = True)
write_tour_to_file(tour, '_evolutionary_0')


startTime = time.time()

for i in range(0, len(solutions)):
    sol = solutions[i]
    trueCost = completeCost(sol[1], sol[0], graph[0], directedEdges, costDict, pathDict)

    tour = repair(sol[1], sol[0], trueCost, inits, graph)

    write_tour_to_file(tour, '_evolutionary_' + str(i+1))







