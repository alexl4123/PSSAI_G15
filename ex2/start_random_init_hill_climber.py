from src.graph_data_structs import *
from src.parse_input_file import parse_input_file

from src.metasearch_init_procedure import generalInitialization, initSolutions, randomizedInit
from src.metasearch_common_procedures import *
from src.hill_climbing import * 


# Parse input file (file from args)
graph = parse_input_file()
inits = generalInitialization(graph)

curBest = -1
bestSolL = []
bestSolD = {}

print("<<<<<<<<<<<<<<<")
maxIter = 100000


maxTime = 5
startTime = time.time()

for i in range(0, maxIter):
    if not isInTime(startTime, maxTime):
        break

    print("Iter " + str(i) + " of " + str(maxIter))

    (solL, solD) = initSolutions(inits[0])
    randomizedInit(solL)

    (solD, solL, bestSolCost) = hillClimber(graph, inits, (solL, solD), startTime = startTime, maxTime = maxTime)
    
    print(">> GOT: " + str(bestSolCost[0][3]) + ", CUR BEST: " + str(curBest) + "<<")

    if (bestSolCost[0][3] < curBest) or curBest == -1:
        curBest = bestSolCost[0][3]
        bestSolL = solL
        bestSolD = solD

print("<<<<<<<<<<<<<<<")
tour = repair(bestSolD, bestSolL, bestSolCost, inits, graph, verbose = True)
write_tour_to_file(tour, '_randomized_hill_climber')


