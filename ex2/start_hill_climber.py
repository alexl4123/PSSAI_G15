from src.graph_data_structs import *
from src.parse_input_file import parse_input_file

from src.metasearch_init_procedure import *
from src.metasearch_common_procedures import *
from src.hill_climbing import * 


# Parse input file (file from args)
graph = parse_input_file()
inits = generalInitialization(graph)


(solL, solD) = initSolutions(inits[0])
#randomizedInit(solL)
(directedEdges, costDict, pathDict, verticesD, avgPerViolation) = inits
(solL, solD) = initGreedySolutions(inits, graph)

cost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
print('Cur cost 3: ' + str(cost))
 
(solD, solL, bestSolCost) = hillClimber(graph, inits, (solL, solD), maxTime = 10)

cost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
print('Cur cost 4: ' + str(cost))
 


tour = repair(solD, solL, bestSolCost, inits, graph, verbose = True)
write_tour_to_file(tour, '_hill_climber')


