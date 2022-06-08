from src.graph_data_structs import *
from src.parse_input_file import parse_input_file

from src.metasearch_init_procedure import generalInitialization, initSolutions, randomizedInit
from src.metasearch_common_procedures import *
from src.hill_climbing import * 


# Parse input file (file from args)
graph = parse_input_file()
inits = generalInitialization(graph)


(solL, solD) = initSolutions(inits[0])
randomizedInit(solL)

(solD, solL, bestSolCost) = hillClimber(graph, inits, (solL, solD))


tour = repair(solD, solL, bestSolCost, inits, graph)
write_tour_to_file(tour, '_hill_climber')


