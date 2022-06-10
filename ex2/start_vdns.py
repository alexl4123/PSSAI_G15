from src.graph_data_structs import *
from src.parse_input_file import parse_input_file

from src.metasearch_init_procedure import *
from src.metasearch_common_procedures import *
from src.hill_climbing import * 
from src.vdns import * 


# Parse input file (file from args)
graph = parse_input_file()
inits = generalInitialization(graph)
(directedEdges, costDict, pathDict, verticesD, avgPerViolation) = inits


#(solL, solD) = initGreedySolutions(inits, graph)

curBestSol = None
curBestCost = ((0,0,0,-1),1)

maxTime = 6000
startTime = time.time()
for i in range(0, 1000):
    if not isInTime(startTime,maxTime):
        break
    (solL, solD) = initSolutions(inits[0])
    randomizedInit(solL)

    cost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
    print('Cur cost 3: ' + str(cost))
     
    (solD, solL, bestSolCost) = vdns(graph, inits, (solL, solD), startTime = startTime, maxTime = maxTime)

    cost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
    print('Cur cost 4: ' + str(cost))

    if curBestCost[0][3] == -1 or cost[0][3] < curBestCost[0][3]:
        curBestCost = cost
        curBestSol = (solD, solL, bestSolCost)
        print("<Accepted with: " + str(curBestCost[0][3]) + ">")
     

print("<<<BEST SOL WITH COST: " + str(curBestCost[0][3]) + ">>>")

tour = repair(curBestSol[0], curBestSol[1], curBestSol[2], inits, graph, verbose = True)
write_tour_to_file(tour, '_vdns')

