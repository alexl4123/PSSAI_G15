import sys
import time
import copy
import ast

from src.metasearch_init_procedure import initSolutions

def loadSolution(path):
    input_file_path = path
    input_file = open(input_file_path, "r")
    list_ = input_file.readline()
    input_file.close()

    list_ = ast.literal_eval(list_)

    return (list_)


def parseSolution(list_, directedEdges):
    
    sol = initSolutions(directedEdges)
    (solL, solD) = sol

    for i in range(1, len(list_)):
        solD[str(list_[i-1]) + ':' + str(list_[i])].incX()

    return sol

def loadAndParseSolution(path, directedEdges):
    list_ = loadSolution(path)


    sol = parseSolution(list_, directedEdges)

    return sol


