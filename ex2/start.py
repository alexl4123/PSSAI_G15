from graph_data_structs import *
from parse_input_file import parse_input_file

from metasearch_init_procedure import generalInitialization
from hill_climbing import * 


# Parse input file (file from args)
graph = parse_input_file()
inits = generalInitialization(graph)
(solD, solL, bestSolCost) = hillClimber(graph, inits)
tour = repair(solD, solL, bestSolCost, inits, graph)
write_tour_to_file(tour)


