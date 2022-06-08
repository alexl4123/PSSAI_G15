import random 

from src.graph_data_structs import *
from src.parse_input_file import parse_input_file

from src.metasearch_init_procedure import generalInitialization, initSolutions, randomizedInit
from src.metasearch_common_procedures import *
from src.hill_climbing import * 

# ------------------------------------------EVOLUTIONARY-ALG----------------------------

def generateSolutions(solutions, evals):
    newSolutions = []
    newSolutionsChanges = []
    newSolutionsEvaluation = []

    for i in range(0, len(solutions)):
        newSolutions.append(solutions[i])
        newSolutionsChanges.append([])
        newSolutionsEvaluation.append(evals[i])

    # Crossover
    for i in range(0,len(solutions)):
        for j in range(0, len(solutions)):
            if (i == j):
                next
            
            newSolution = cloneSolutions(solutions[i][0])
            newSolutionChanges = []

            # Accept 0.05 - 0.2 percent of another solution
            lower = random.uniform(0,0.8)
            upper = random.uniform(lower+0.05,lower+0.2)

            lowerIndex = int(lower * len(solutions[i][0]))
            upperIndex = int(upper * len(solutions[i][0]))

            if lowerIndex == upperIndex:
                next

            for k in range(lowerIndex, upperIndex):
                newSolutionChanges.append((newSolution[0][k][0], newSolution[0][k][1], solutions[j][0][k][2].getX() - newSolution[0][k][2].getX()))
                newSolution[0][k][2].set(solutions[j][0][k][2].getX())

            newSolutions.append(newSolution)
            newSolutionsChanges.append(newSolutionChanges)
            newSolutionsEvaluation.append(evals[i])

    # Mutation

    for i in range(0, len(solutions)):
        percentage = random.uniform(0.1,0.25)

        newSolution = cloneSolutions(solutions[i][0])
        newSolutionChanges = []

        lower = random.uniform(0,1 - percentage)
        upper = lower + percentage

        lowerIndex = int(lower * len(solutions[i][0]))
        upperIndex = int(upper * len(solutions[i][0]))

        if lowerIndex == upperIndex:
            next

        for k in range(lowerIndex, upperIndex):
            newValue = random.randint(0,2)
            newSolutionChanges.append((newSolution[0][k][0], newSolution[0][k][1], newValue - newSolution[0][k][2].getX()))
            newSolution[0][k][2].set(newValue)

        newSolutions.append(newSolution)
        newSolutionsChanges.append(newSolutionChanges)
        newSolutionsEvaluation.append(evals[i])

    return (newSolutions, newSolutionsChanges, newSolutionsEvaluation)

def evaluateSolutions(newSols, verticesD, avgCs3Cost):
    newSolutions = newSols[0]
    newSolutionsChanges = newSols[1]
    newSolutionsEvaluation = newSols[2]

    result = []

    for i in range(0, len(newSolutions)):
        curCost = iterativeCost(newSolutions[i][1], newSolutions[i][0], verticesD, newSolutionsEvaluation[i], newSolutionsChanges[i], avgCs3Cost)

        result.append((curCost, newSolutions[i]))

    return result

# ------------------------------------------EVOLUTIONARY-ALG-END----------------------------
# Parse input file (file from args)
graph = parse_input_file()
inits = generalInitialization(graph)
# ------------------------------------------EVOLUTIONARY-ALG----------------------------
populationSize = 5
maxIter = 10


# Generate Initial Solutions


(directedEdges, costDict, pathDict, verticesD, avgPerViolation) = inits

solutions = []
evaluations = []
for i in range(0, populationSize):
    sol = initSolutions(inits[0])
    randomizedInit(sol[0])
    solutions.append(sol)
    evaluations.append(completeCost(sol[1], sol[0], graph[0], directedEdges, costDict, pathDict))


for i in range(0, maxIter):
    newSols = generateSolutions(solutions, evaluations)
    
    solEvals = evaluateSolutions(newSols, verticesD, avgPerViolation)

    solEvals.sort(key = lambda x: x[0][0][3])


    print('<<<Iteration ' + str(i))
    solutions = []
    evaluations = []

    for j in range(0, populationSize):
        print('    Accepted with cost ' + str(solEvals[j][0][0][3]))
        solutions.append(solEvals[j][1])
        evaluations.append(solEvals[j][0])

    if (i+1) % 5 == 0:
        # Every 5 iterations recalculate the cost exactly
        evaluations = []
        for j in range(0, populationSize):
            sol = solutions[j]
            evaluations.append(completeCost(sol[1], sol[0], graph[0], directedEdges, costDict, pathDict))
    
    print('>>>')



# ------------------------------------------EVOLUTIONARY-ALG----------------------------

for i in range(0, populationSize):
    sol = solutions[i]
    trueCost = completeCost(sol[1], sol[0], graph[0], directedEdges, costDict, pathDict)

    tour = repair(sol[1], sol[0], trueCost, inits, graph)

    write_tour_to_file(tour, '_evolutionary_' + str(i))


